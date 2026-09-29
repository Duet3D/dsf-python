# Duet Software Framework Python Bindings

`dsf-python` is a Python client for the [Duet Software Framework](https://github.com/Duet3D/DuetSoftwareFramework)
(DSF) control server. It talks to DSF over its UNIX socket and provides:

- `dsf.connections`: connections for sending commands, subscribing to the object model and intercepting codes
- `dsf.object_model`: the DSF object model as typed Python classes
- `dsf.http`: custom HTTP and WebSocket endpoints served through DSF
- `dsf.commands`: low-level builders for every DSF command

It follows the C# `DuetAPIClient` closely, but uses Python naming. See
[Differences from the DSF API](#differences-from-the-dsf-api) before porting C# code or reading the DSF docs.

- [Examples](https://github.com/Duet3D/dsf-python/tree/HEAD/examples)
- [PyPI package](https://pypi.org/project/dsf-python/)
- [DSF forum](https://forum.duet3d.com/category/31/dsf-development)

## Installation

```bash
python3 -m pip install dsf-python
```

Python 3.11 or newer is required. Your script must run on the machine that runs DSF, as a user
that can access the DSF socket (usually the `dsf` user). The socket path is read from
`/opt/dsf/conf/config.json` and falls back to `/run/dsf/dcs.sock`.

## Quick Start

```python
from dsf.connections import CommandConnection

connection = CommandConnection()
connection.connect()
try:
    print(connection.perform_simple_code("M115"))

    object_model = connection.get_object_model()
    print(object_model.state.status.value)
    print(object_model.state.up_time)       # "upTime" in DSF
finally:
    connection.close()
```

## Connections

| Connection | Use it to | Example |
|---|---|---|
| `CommandConnection` | Run codes, evaluate expressions, read the object model, manage plugins, files and HTTP endpoints | [send_commands.py](https://github.com/Duet3D/dsf-python/blob/HEAD/examples/send_commands.py) |
| `SubscribeConnection` | Keep a local copy of the object model up to date and react to changes | [subscribe_object_model.py](https://github.com/Duet3D/dsf-python/blob/HEAD/examples/subscribe_object_model.py) |
| `InterceptConnection` | Handle custom M-codes, or inspect codes before or after DSF processes them | [custom_m_codes.py](https://github.com/Duet3D/dsf-python/blob/HEAD/examples/custom_m_codes.py) |

Every connection is configured in its constructor, opened with `connect()` and closed with `close()`.
Errors reported by DSF are raised as `InternalServerException` (with `error_type` and `error_message`),
or as `TaskCanceledException` if DSF cancelled the request.

### SubscribeConnection

```python
from dsf.connections import SubscribeConnection, SubscriptionMode

subscription = SubscribeConnection(SubscriptionMode.PATCH, filter_list=["state/status", "heat/heaters[*]/current"])
subscription.connect()

object_model = subscription.get_object_model()  # First call: blocks for the full object model

def on_heater_changed(*, key, data, indices):
    print(f"Heater {indices[0]} is now at {data}C")

unsubscribe = subscription.subscribe_to_keys(["heat.heaters.^.current"], on_heater_changed)

while True:
    object_model = subscription.get_object_model()  # Later calls: apply queued patches, run callbacks
    ...
```

- In `SubscriptionMode.PATCH`, the first `get_object_model()` call blocks until the full model arrives.
  Later calls do not block: they apply every queued patch to the cached model and return it.
- In `SubscriptionMode.FULL`, every call blocks until the next full object model arrives.
- `subscribe_to_keys()` callbacks run synchronously inside `get_object_model()`, only in patch mode, and
  receive the keyword arguments `key`, `data` (the raw JSON value from the patch) and `indices` (the list
  indexes matched by `^`, or `None`). Register them after the first `get_object_model()` call.
  The return value removes the callback again.

### InterceptConnection

```python
from dsf.connections import InterceptConnection, InterceptionMode
from dsf.object_model import MessageType

interceptor = InterceptConnection(InterceptionMode.PRE, filters=["M1234"])
interceptor.connect()
while True:
    code = interceptor.receive_code()
    name = code.parameter("S", "world").string_value
    interceptor.resolve_code(MessageType.Success, f"Hello {name}!")
```

Every intercepted code must be answered with `resolve_code()`, `ignore_code()` or `cancel_code()`.
`InterceptConnection` also has all `CommandConnection` methods, so it can run other codes while a
code is intercepted, e.g. `perform_simple_code("M117 hi", code.channel)`.

### Custom HTTP Endpoints

```python
from dsf.http import HttpEndpointConnection, HttpResponseType
from dsf.object_model import HttpEndpointType

async def hello(connection: HttpEndpointConnection) -> None:
    request = await connection.read_request()
    await connection.send_response(200, f"Hello {request.queries.get('name', 'world')}!", HttpResponseType.PlainText)

endpoint = command_connection.add_http_endpoint(HttpEndpointType.GET, "example", "hello")
endpoint.set_endpoint_handler(hello)  # Serves GET /machine/example/hello in a background thread
...
command_connection.remove_http_endpoint(HttpEndpointType.GET, "example", "hello")
endpoint.close()
```

See [custom_http_endpoint.py](https://github.com/Duet3D/dsf-python/blob/HEAD/examples/custom_http_endpoint.py).

## Differences From The DSF API

### Naming

Python attributes and methods are `snake_case`. **Anything passed to DSF as a string stays in DSF's
`camelCase` format**, because DSF interprets it and not this library.

| | DSF / C# | dsf-python |
|---|---|---|
| Object model properties | `state.upTime`, `move.axes[0].userPosition` | `state.up_time`, `move.axes[0].user_position` |
| Uppercase acronyms | `move.skew.tanXY` | `move.skew.tan_XY` (acronyms stay uppercase) |
| Global variables | `global` | `globals` (`global` is a Python keyword) |
| Names shadowing builtins (`type`, `id`, `min`, `max`, `format`, `license`) | `axis.max` | `axis.max` (unchanged) |
| Methods | `PerformSimpleCodeAsync()` | `perform_simple_code()` |
| Intercepted `Code` attributes | `MajorNumber`, `KeywordArgument` | `majorNumber`, `keywordArgument` (**camelCase, as in the JSON**) |
| `CodeParameter` attributes | `StringValue`, `IsString` | `string_value`, `is_string` |
| HTTP request fields | `SessionId`, `ContentType` | `session_id`, `content_type` |
| Error responses | `errorType`, `errorMessage` | `error_type`, `error_message` |
| Enum members | `MessageType.Success` | Not normalised: `MessageType.Success`, `MachineStatus.idle`, `SubscriptionMode.PATCH`, `HttpEndpointType.GET`. Values match the DSF JSON. |

These strings keep DSF naming:

| Where | Format | Example |
|---|---|---|
| `SubscribeConnection(filter_list=...)` | `/`-separated, `[*]` for any list item, `**` for everything below | `"heat/heaters[*]/current"`, `"move/**"` |
| `CommandConnection.get_object_model(filters)` | `.`-separated key paths | `["state", "move.axes"]` |
| `SubscribeConnection.subscribe_to_keys(keys)` | `.`-separated, list indexes as numbers, `^` for any list item | `"heat.heaters.^.current"`, `"move.axes.2.userPosition"` |
| `evaluate_expression()`, `query_object_model()`, G-code | RepRapFirmware expressions | `"state.upTime"`, `"move.axes[0].homed"` |

`ObjectModel.update_from_json()` and `from_json()` take DSF JSON (`camelCase`), and `to_json()` writes it back:

```python
object_model.update_from_json({"state": {"upTime": 1234}})
object_model.state.up_time    # 1234
object_model.to_json()        # '{..."state": {..."upTime": 1234...}...}'
```

### Behaviour

- **Synchronous.** Connection methods block and have no `Async` suffix or `CancellationToken`.
  Only HTTP endpoint handlers are `async` coroutines.
- **Configuration in the constructor.** Options passed to C# `ConnectAsync()` (mode, filters, channels,
  `verbose`, ...) are constructor arguments. `connect()` takes only an optional socket path.
- **Patches are applied for you.** `SubscribeConnection.get_object_model()` keeps an internal model up
  to date in patch mode. In C#, you apply patches from `GetObjectModelPatchAsync()` yourself.
  `get_object_model_patch()` and `get_serialized_object_model()` still return raw JSON if you need it.
- **Key callbacks** (`subscribe_to_keys()`) are specific to dsf-python.
- **Return values.** `perform_simple_code()` returns the reply as a string. `evaluate_expression()`
  and the lower-level methods return a `Response` whose value is in `.result`.
- **Interception.** `resolve_code()` takes a `MessageType` and an optional string, not a `Message`.
  There is no `rewrite_code()`. `flush()` takes a channel instead of flushing the intercepted code's channel.
- **HTTP endpoints.** Handlers are registered with `set_endpoint_handler()` instead of an event.
  `add_http_endpoint()` returns an `HttpEndpointUnixSocket`, which must be closed after
  `remove_http_endpoint()`.

## Examples

| Example | Shows |
|---|---|
| [send_commands.py](https://github.com/Duet3D/dsf-python/blob/HEAD/examples/send_commands.py) | Run codes, evaluate expressions, read part of the object model, write messages, handle errors |
| [subscribe_object_model.py](https://github.com/Duet3D/dsf-python/blob/HEAD/examples/subscribe_object_model.py) | Filtered patch subscription, key callbacks with and without `^` |
| [custom_m_codes.py](https://github.com/Duet3D/dsf-python/blob/HEAD/examples/custom_m_codes.py) | Custom M-codes, reading parameters, running codes from an interceptor |
| [custom_http_endpoint.py](https://github.com/Duet3D/dsf-python/blob/HEAD/examples/custom_http_endpoint.py) | GET and POST endpoints with plain text and JSON responses |

## Development

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest                               # Tests use mock DSF sockets, no DSF install needed
sphinx-build -b html docs/source docs/build     # API reference
```
