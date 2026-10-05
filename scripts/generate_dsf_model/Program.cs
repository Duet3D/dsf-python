// Generates the reference object model data used by tests/test_dsf_model.py from the DuetAPI object model,
// so the tests follow DSF instead of a hand-maintained copy.
//
// Usage (see the Makefile target generate_dsf_model):
//   dotnet run --project scripts/generate_dsf_model -p:DsfPath=<DuetSoftwareFramework checkout> -- <output.json>
//
// For every object model class the output contains:
//   properties: JSON name => whether it is nullable
//   base:       for dynamic model objects, the class DSF deserializes them through
//   create:     for dynamic model objects, the JSON that makes DSF create this class
//   default:    a new instance, created the same way as DSF does when deserializing
//   values:     every property set to a sample value and every collection/dictionary given items
//   nulls:      every nullable property and collection item set to null, the others set to different sample values,
//               and dictionary items that "values" has set to null
//   patched:    the result of DSF updating a new instance from "values" and then from "nulls"
// The "dynamic" list holds the class and JSON DSF produces for every discriminator value of dynamic model objects.
// The "runtimeDefaults" list holds the properties left out of "default" because they depend on when or where DSF runs.
// All JSON above is written by DSF's own serializer (ObjectModelContext).
//
// The "enums" object holds every public enum of DuetAPI (all namespaces) by its name:
//   namespace: namespace of the enum
//   flags:     whether it is a [Flags] enum
//   members:   every member in declaration order (including members sharing a value with another one), each with
//              name:  C# name
//              value: underlying integer value
//              json:  the JSON DSF writes for it with its default options (JsonHelper.DefaultJsonOptions),
//                     or "error" instead if DSF cannot write it
//   error:     only present if DSF cannot write the enum at all because it is not part of any of its JSON contexts,
//              its members have no "json" then

using System.Collections;
using System.Reflection;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Serialization.Metadata;
using DuetAPI.ObjectModel;
using DuetAPI.Utility;

if (args.Length != 1)
{
    Console.Error.WriteLine("Usage: dotnet run --project scripts/generate_dsf_model -p:DsfPath=<DuetSoftwareFramework> -- <output.json>");
    return 1;
}

JsonSerializerOptions options = ObjectModelContext.Default.Options;
NullabilityInfoContext nullabilityContext = new();

// Properties DSF uses to pick the class of dynamic model objects when deserializing them
Dictionary<Type, string> discriminators = new()
{
    [typeof(DirectDisplayScreen)] = "controller",
    [typeof(FilamentMonitor)] = "type",
    [typeof(Kinematics)] = "name"
};

// Dynamic model objects whose discriminator is deliberately read case-insensitively by DSF,
// because the firmware reports some kinematics names capitalized
HashSet<Type> caseInsensitiveDiscriminators = [typeof(Kinematics)];

// Defaults that depend on when or where DSF runs rather than on the object model
HashSet<string> runtimeDefaults =
[
    "DSF.version",      // Version of the running DSF
    "Message.time"      // Time the message was created
];

List<Type> modelClasses = [];
foreach (Type type in typeof(ObjectModel).Assembly.GetTypes().Where(IsModelClass).OrderBy(type => type.Name, StringComparer.Ordinal))
{
    if (IsJsonObject(type))
    {
        modelClasses.Add(type);
    }
    else
    {
        // Not reachable from the object model on its own (e.g. a base class), so it is never serialized as such
        Console.Error.WriteLine($"Skipping {type.Name}: not part of {nameof(ObjectModelContext)}");
    }
}

JsonObject classes = [];
foreach (Type type in modelClasses)
{
    JsonTypeInfo typeInfo = options.GetTypeInfo(type);

    JsonObject properties = [];
    foreach (JsonPropertyInfo property in typeInfo.Properties)
    {
        properties[property.Name] = new JsonObject { ["nullable"] = IsNullable(property) };
    }

    JsonObject dsfClass = new() { ["properties"] = properties };
    Type? baseType = GetDynamicBaseType(type);
    if (baseType is not null)
    {
        dsfClass["base"] = baseType.Name;
        dsfClass["create"] = GetCreateJson(type);
    }

    object defaultModel = Create(type);
    JsonNode defaults = Serialize(defaultModel);
    Visit(defaultModel, defaults, RemoveRuntimeDefaults);
    dsfClass["default"] = defaults;

    JsonNode values = Serialize(Populate(Create(type), false, 0));
    object nullsModel = Populate(Create(type), true, 0);
    JsonNode nulls = Serialize(nullsModel);
    Visit(nullsModel, nulls, AddRemovedItems);
    dsfClass["values"] = values;
    dsfClass["nulls"] = nulls;

    // DSF must read the values back unchanged, otherwise they are not valid object model data
    object model = Update(Create(type), values);
    string[] differences = [.. GetDifferences(values, Serialize(model), type.Name)];
    if (differences.Length > 0)
    {
        throw new InvalidOperationException($"DSF does not read back the values of {type.Name}:\n{string.Join('\n', differences)}");
    }
    dsfClass["patched"] = Serialize(Update(model, nulls));

    classes[type.Name] = dsfClass;
}

JsonArray dynamic = [];
foreach ((Type baseType, string discriminator) in discriminators.OrderBy(item => item.Key.Name, StringComparer.Ordinal))
{
    foreach (JsonNode value in GetDiscriminatorInputs(baseType, discriminator))
    {
        JsonObject json = new() { [discriminator] = value };
        JsonObject entry = new() { ["base"] = baseType.Name, ["json"] = json.DeepClone() };
        try
        {
            IDynamicModelObject? model = ((IDynamicModelObject)Activator.CreateInstance(baseType)!).UpdateFromJson(JsonSerializer.SerializeToElement(json), false);
            entry["class"] = model?.GetType().Name;
            entry["result"] = model is null ? null : Serialize(model);
        }
        catch (Exception e)
        {
            // DSF rejects this value
            entry["error"] = e.GetType().Name;
        }
        dynamic.Add(entry);
    }
}

JsonObject enums = [];
foreach (Type type in typeof(ObjectModel).Assembly.GetTypes().Where(IsPublicEnum).OrderBy(type => type.Name, StringComparer.Ordinal))
{
    if (enums.ContainsKey(type.Name))
    {
        throw new InvalidOperationException($"More than one public enum is called {type.Name}");
    }

    // Not part of any JSON context, so DSF never reads or writes it (e.g. enums used internally by DuetAPI)
    bool serializable = JsonHelper.DefaultJsonOptions.TryGetTypeInfo(type, out _);

    JsonArray members = [];
    // Fields rather than Enum.GetValues so members sharing a value with another one are listed as well
    foreach (FieldInfo field in type.GetFields(BindingFlags.Public | BindingFlags.Static).OrderBy(field => field.MetadataToken))
    {
        JsonObject member = new()
        {
            ["name"] = field.Name,
            ["value"] = Convert.ToInt64(field.GetRawConstantValue())
        };
        if (serializable)
        {
            try
            {
                member["json"] = JsonSerializer.SerializeToNode(field.GetValue(null), type, JsonHelper.DefaultJsonOptions);
            }
            catch (Exception e)
            {
                // DSF cannot write this value
                member["error"] = $"{e.GetType().Name}: {e.Message}";
            }
        }
        members.Add(member);
    }

    JsonObject dsfEnum = new()
    {
        ["namespace"] = type.Namespace,
        ["flags"] = type.IsDefined(typeof(FlagsAttribute), false),
        ["members"] = members
    };
    if (!serializable)
    {
        dsfEnum["error"] = "Not part of any JSON context of DSF";
    }
    enums[type.Name] = dsfEnum;
}

JsonObject output = new()
{
    ["dsfVersion"] = typeof(ObjectModel).Assembly.GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion,
    ["classes"] = classes,
    ["dynamic"] = dynamic,
    ["runtimeDefaults"] = new JsonArray([.. runtimeDefaults.Order(StringComparer.Ordinal).Select(name => JsonValue.Create(name))]),
    ["enums"] = enums
};
File.WriteAllText(args[0], output.ToJsonString(new JsonSerializerOptions(options) { WriteIndented = true }) + "\n");
Console.WriteLine($"Wrote {classes.Count} classes, {dynamic.Count} dynamic cases and {enums.Count} enums to {args[0]}");
return 0;

IEnumerable<string> GetDifferences(JsonNode? expected, JsonNode? actual, string path)
{
    if (expected is JsonObject expectedObject && actual is JsonObject actualObject)
    {
        return expectedObject.Select(item => item.Key).Union(actualObject.Select(item => item.Key))
            .SelectMany(key => GetDifferences(expectedObject[key], actualObject[key], $"{path}.{key}"));
    }
    if (expected is JsonArray expectedArray && actual is JsonArray actualArray && expectedArray.Count == actualArray.Count)
    {
        return expectedArray.Zip(actualArray).SelectMany((items, index) => GetDifferences(items.First, items.Second, $"{path}[{index}]"));
    }
    return JsonNode.DeepEquals(expected, actual) ? [] : [$"{path}: {expected?.ToJsonString() ?? "null"} => {actual?.ToJsonString() ?? "null"}"];
}

// Public enums, including ones nested in public classes
bool IsPublicEnum(Type type) => type.IsEnum && type.IsVisible;

bool IsModelClass(Type type) =>
    type is { IsClass: true, IsAbstract: false, IsPublic: true, ContainsGenericParameters: false, Namespace: "DuetAPI.ObjectModel" } &&
    (type.IsSubclassOf(typeof(ModelObject)) || IsJsonObject(type));

// Object model classes are serialized as JSON objects, unlike values, collections and dictionaries
bool IsJsonObject(Type type) => options.TryGetTypeInfo(type, out JsonTypeInfo? typeInfo) && typeInfo.Kind == JsonTypeInfoKind.Object;

PropertyInfo GetPropertyInfo(JsonPropertyInfo property) => (PropertyInfo)property.AttributeProvider!;

bool IsNullable(JsonPropertyInfo property) =>
    Nullable.GetUnderlyingType(property.PropertyType) is not null ||
    nullabilityContext.Create(GetPropertyInfo(property)).ReadState == NullabilityState.Nullable;

JsonNode Serialize(object value) => JsonSerializer.SerializeToNode(value, options.GetTypeInfo(value.GetType()))!;

Type? GetDynamicBaseType(Type type) => discriminators.Keys.FirstOrDefault(baseType => baseType.IsAssignableFrom(type));

// Classes DSF may create for a dynamic model object, the base class first
IEnumerable<Type> GetDynamicTypes(Type baseType) =>
    modelClasses.Where(baseType.IsAssignableFrom).OrderBy(type => type != baseType).ThenBy(type => type.Name, StringComparer.Ordinal);

JsonPropertyInfo GetDiscriminatorProperty(Type baseType) =>
    options.GetTypeInfo(baseType).Properties.First(property => property.Name == discriminators[baseType]);

// Every discriminator value as written by DSF, lower-cased where the firmware may report it so, and an unknown one
IEnumerable<JsonNode> GetDiscriminatorInputs(Type baseType, string discriminator)
{
    Type discriminatorType = GetDiscriminatorProperty(baseType).PropertyType;
    List<JsonNode> inputs = [];
    foreach (object value in Enum.GetValues(discriminatorType))
    {
        JsonNode node = JsonSerializer.SerializeToNode(value, discriminatorType, options)!;
        inputs.Add(node);
        if (caseInsensitiveDiscriminators.Contains(baseType) && node.GetValueKind() == JsonValueKind.String)
        {
            inputs.Add(JsonValue.Create(node.GetValue<string>().ToLowerInvariant()));
        }
    }
    inputs.Add(JsonValue.Create("unknownValue"));
    return inputs.DistinctBy(node => node.ToJsonString());
}

// JSON that makes DSF create the given dynamic model object, preferring the default discriminator value
JsonObject GetCreateJson(Type type)
{
    Type baseType = GetDynamicBaseType(type)!;
    string discriminator = discriminators[baseType];
    JsonPropertyInfo discriminatorProperty = GetDiscriminatorProperty(baseType);
    object defaultValue = discriminatorProperty.Get!(Activator.CreateInstance(baseType)!)!;
    foreach (object value in Enum.GetValues(discriminatorProperty.PropertyType).Cast<object>().Prepend(defaultValue))
    {
        JsonObject json = new() { [discriminator] = JsonSerializer.SerializeToNode(value, discriminatorProperty.PropertyType, options) };
        if (UpdateDynamic(Activator.CreateInstance(baseType)!, json)?.GetType() == type)
        {
            return json;
        }
    }
    throw new NotSupportedException($"No {discriminator} of {baseType.Name} makes DSF create a {type.Name}");
}

IDynamicModelObject? UpdateDynamic(object model, JsonNode json) =>
    ((IDynamicModelObject)model).UpdateFromJson(JsonSerializer.SerializeToElement(json), false);

// Create a model object like DSF does, i.e. dynamic model objects are created from the discriminator selecting their class
object Create(Type type)
{
    Type? baseType = GetDynamicBaseType(type);
    return (baseType is null) ? Activator.CreateInstance(type)! : UpdateDynamic(Activator.CreateInstance(baseType)!, GetCreateJson(type))!;
}

// Update a model object from JSON the same way DSF applies object model patches
object Update(object model, JsonNode json)
{
    switch (model)
    {
        case IDynamicModelObject dynamicModel:
            return dynamicModel.UpdateFromJson(JsonSerializer.SerializeToElement(json), false)
                ?? throw new InvalidOperationException($"DSF discarded {model.GetType().Name}");
        case IStaticModelObject staticModel:
            staticModel.UpdateFromJson(JsonSerializer.SerializeToElement(json), false);
            return model;
        default:
            // Not updated in place by DSF (e.g. messages), only deserialized as a whole
            return JsonSerializer.Deserialize(json, options.GetTypeInfo(model.GetType()))!;
    }
}

// Call the visitor for every model object, dictionary and list along with the JSON it was serialized to
void Visit(object? model, JsonNode? json, Action<object, JsonNode> visitor)
{
    if (model is null || json is null)
    {
        return;
    }

    visitor(model, json);
    if (IsJsonObject(model.GetType()) && json is JsonObject jsonObject)
    {
        foreach (JsonPropertyInfo property in options.GetTypeInfo(model.GetType()).Properties)
        {
            Visit(property.Get!(model), jsonObject[property.Name], visitor);
        }
    }
    else if (model is IDictionary dictionary && json is JsonObject items)
    {
        // Not enumerated directly because JsonModelDictionary does not enumerate DictionaryEntry items
        foreach (string key in dictionary.Keys)
        {
            Visit(dictionary[key], items[key], visitor);
        }
    }
    else if (model is IList list && json is JsonArray array)
    {
        for (int index = 0; index < list.Count; index++)
        {
            Visit(list[index], array[index], visitor);
        }
    }
}

// Remove the defaults that depend on when or where DSF runs
void RemoveRuntimeDefaults(object model, JsonNode json)
{
    if (IsJsonObject(model.GetType()) && json is JsonObject jsonObject)
    {
        foreach (JsonPropertyInfo property in options.GetTypeInfo(model.GetType()).Properties)
        {
            if (runtimeDefaults.Contains($"{model.GetType().Name}.{property.Name}"))
            {
                jsonObject.Remove(property.Name);
            }
        }
    }
}

// Dictionaries that remove items set to null cannot hold them, so add them to the JSON
void AddRemovedItems(object model, JsonNode json)
{
    if (model is IModelDictionary && json is JsonObject jsonObject)
    {
        jsonObject["removed"] = null;
    }
}

// Set every property of a model object to a sample value, or to null if requested and allowed
object Populate(object model, bool nulls, int depth)
{
    JsonTypeInfo typeInfo = options.GetTypeInfo(model.GetType());
    if (depth > 20)
    {
        throw new InvalidOperationException($"Object model nested too deeply at {typeInfo.Type.Name}");
    }

    Type? dynamicBaseType = GetDynamicBaseType(typeInfo.Type);
    for (int index = 0; index < typeInfo.Properties.Count; index++)
    {
        JsonPropertyInfo property = typeInfo.Properties[index];
        string name = $"{typeInfo.Type.Name}.{property.Name}";
        // Sample values depend on the property's position so mixed up properties are detected
        int seed = index + 1;
        Type type = Nullable.GetUnderlyingType(property.PropertyType) ?? property.PropertyType;
        object? current = property.Get!(model);

        if (dynamicBaseType is not null && discriminators[dynamicBaseType] == property.Name)
        {
            // Changing it would make DSF create a different class
            continue;
        }

        if (nulls && property.Set is not null && IsNullable(property))
        {
            property.Set(model, null);
        }
        else if (IsJsonObject(type))
        {
            // Use a derived class for dynamic model objects so switching to it is covered as well
            Type valueType = (GetDynamicBaseType(type) is not null && property.Set is not null) ? GetDynamicTypes(type).Last() : type;
            object value = (current?.GetType() == valueType) ? current : Create(valueType);
            Populate(value, nulls, depth + 1);
            if (!ReferenceEquals(value, current))
            {
                SetProperty(property, model, value, name);
            }
        }
        else if (typeof(IDictionary).IsAssignableFrom(type) || (typeof(IList).IsAssignableFrom(type) && !type.IsArray))
        {
            object value = current ?? Activator.CreateInstance(type)!;
            NullabilityInfo[] itemNullability = nullabilityContext.Create(GetPropertyInfo(property)).GenericTypeArguments;
            bool nullableItems = itemNullability.Length > 0 && itemNullability[^1].ReadState == NullabilityState.Nullable;
            if (value is IDictionary dictionary)
            {
                dictionary.Clear();
                Type itemType = GetGenericArgument(type, typeof(IDictionary<,>), 1, name);
                dictionary["key"] = CreateItems(null, itemType, nulls, depth, name, seed).First();
                if (!nulls)
                {
                    // Set to null by "nulls" to cover removing items
                    dictionary["removed"] = CreateItems(null, itemType, nulls, depth, name, seed).First();
                }
            }
            else
            {
                IList list = (IList)value;
                list.Clear();
                Type itemType = GetGenericArgument(type, typeof(IList<>), 0, name);
                if (nulls && (nullableItems || Nullable.GetUnderlyingType(itemType) is not null))
                {
                    list.Add(null);
                }
                foreach (object item in CreateItems(list, itemType, nulls, depth, name, seed))
                {
                    list.Add(item);
                }
            }
            if (current is null)
            {
                SetProperty(property, model, value, name);
            }
        }
        else if (property.Set is not null)
        {
            property.Set(model, Sample(type, current, name, seed, nulls));
        }
        // else the value is fixed by the class, e.g. CoreKinematics.Name
    }
    return model;
}

void SetProperty(JsonPropertyInfo property, object model, object? value, string name)
{
    if (property.Set is null)
    {
        throw new NotSupportedException($"{name} is read-only and cannot be populated");
    }
    property.Set(model, value);
}

Type GetGenericArgument(Type type, Type genericInterface, int index, string name)
{
    Type? match = type.GetInterfaces().Append(type).FirstOrDefault(i => i.IsGenericType && i.GetGenericTypeDefinition() == genericInterface);
    return match?.GetGenericArguments()[index] ?? throw new NotSupportedException($"Cannot determine the item type of {name} ({type})");
}

// Items for a collection, i.e. one item of every class DSF may create for it
IEnumerable<object> CreateItems(object? collection, Type itemType, bool nulls, int depth, string name, int seed)
{
    Type type = Nullable.GetUnderlyingType(itemType) ?? itemType;
    if (!IsJsonObject(type))
    {
        return [Sample(type, null, $"{name}[]", seed, nulls)];
    }

    // Collections may create items depending on their position, e.g. the first board is the main board
    MethodInfo? createItem = collection?.GetType().GetMethod("CreateItem", BindingFlags.Instance | BindingFlags.NonPublic, [typeof(int)]);
    if (createItem is not null)
    {
        Type[] itemTypes = [.. Enumerable.Range(0, 4).Select(index => createItem.Invoke(collection, [index])!.GetType())];
        int count = itemTypes.Select(item => Array.IndexOf(itemTypes, item)).Max() + 1;
        return [.. Enumerable.Range(0, count).Select(index => Populate(createItem.Invoke(collection, [index])!, nulls, depth + 1))];
    }
    IEnumerable<Type> types = (GetDynamicBaseType(type) is not null) ? GetDynamicTypes(type) : [type];
    return [.. types.Select(item => Populate(Create(item), nulls, depth + 1))];
}

// Get a sample value of the given type depending on the property's position.
// The "nulls" data gets different values than the "values" data so that the patched values can be told apart
object Sample(Type type, object? current, string name, int seed, bool nulls)
{
    if (type.IsArray)
    {
        Type itemType = type.GetElementType()!;
        Array array = Array.CreateInstance(itemType, 2);
        array.SetValue(Sample(itemType, null, name, seed, nulls), 0);
        array.SetValue(Sample(itemType, array.GetValue(0), name, seed, nulls), 1);
        return array;
    }

    int variant = nulls ? 1 : 0;
    if (type == typeof(bool))
    {
        // Alternate between neighbouring properties and between "values" and "nulls", so every bool
        // takes both values and mixed up properties are detected
        return (seed + variant) % 2 == 1;
    }

    int number = seed + 2 + 100 * variant;
    // 7 significant digits (exact in single precision) so that a loss of precision is detected
    double real = (seed + 10 + 50 * variant) * 1000 + 0.25;
    // Some strings are validated, e.g. plugin identifiers, so only use letters and digits
    string text = new([.. name.Split('.')[^1].Where(char.IsLetterOrDigit)]);
    if (nulls)
    {
        text += "Patched";
    }
    object[] candidates = type switch
    {
        _ when type == typeof(int) => [number, number + 1],
        _ when type == typeof(uint) => [(uint)number, (uint)number + 1],
        _ when type == typeof(char) => nulls ? ['Z', 'Y'] : ['Y', 'Z'],
        _ when type == typeof(byte) => [(byte)number, (byte)(number + 1)],
        _ when type == typeof(short) => [(short)number, (short)(number + 1)],
        _ when type == typeof(ushort) => [(ushort)number, (ushort)(number + 1)],
        _ when type == typeof(ulong) => [(ulong)number, (ulong)number + 1],
        _ when type == typeof(long) => [(long)number, (long)number + 1],
        _ when type == typeof(float) => [(float)real, (float)real + 1],
        _ when type == typeof(double) => [real, real + 1],
        _ when type == typeof(string) => [text, $"{text}2"],
        _ when type == typeof(DateTime) => [new DateTime(2024, 1, 2, 3, 4, 5).AddDays(seed + 100 * variant), new DateTime(2025, 6, 7, 8, 9, 10).AddDays(seed)],
        _ when type == typeof(DriverId) => [new DriverId(1 + variant, seed), new DriverId(3 + variant, seed)],
        _ when type == typeof(JsonElement) => [JsonDocument.Parse($"[{number}, \"{text}\"]").RootElement, JsonDocument.Parse($"{number}").RootElement],
        _ when type == typeof(object) => [number, number + 1],
        // Start at a different enum value for each property, the first one is usually the default
        _ when type.IsEnum => [.. Enum.GetValues(type).Cast<object>().Reverse().Skip((seed + variant) % Enum.GetValues(type).Length),
                               .. Enum.GetValues(type).Cast<object>().Reverse()],
        _ => throw new NotSupportedException($"No sample value for {name} of type {type}, add one to {nameof(Sample)}")
    };
    return candidates.First(candidate => !candidate.Equals(current));
}
