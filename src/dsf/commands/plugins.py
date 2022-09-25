from .basecommands import BaseCommand


def install_plugin(plugin_file: str):
    """
    Install or upgrade a plugin
    :param plugin_file: Absolute file path to the plugin ZIP bundle
    """
    if not isinstance(plugin_file, str) or not plugin_file:
        raise TypeError("plugin_file must be a string")
    return BaseCommand("InstallPlugin", **{"PluginFile": plugin_file})


def set_plugin_data(plugin: str, key: str, value: str):
    """
    Update custom plugin data in the object model
    May be used to update only the own plugin data unless the plugin has the ManagePlugins permission.
    Note that the corresponding key must already exist in the plugin data!
    :param plugin: Identifier of the plugin to update (only mandatory if running as root)
    :param key: Key to set. This key must already exist in the ObjectModel.PluginManifest.Data object!
    :param value: Custom value to set
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    if not isinstance(key, str) or not key:
        raise TypeError("key must be a string")
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return BaseCommand(
        "SetPluginData", **{"Plugin": plugin, "Key": key, "Value": value}
    )


def start_plugin(plugin: str):
    """
    Start a plugin
    :param plugin: Identifier of the plugin
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("StartPlugin", **{"Plugin": plugin})


def stop_plugin(plugin: str):
    """
    Stop a plugin
    :param plugin: Identifier of the plugin
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("StopPlugin", **{"Plugin": plugin})


def uninstall_plugin(plugin: str):
    """
    Uninstall a plugin
    :param plugin: Identifier of the plugin
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("UninstallPlugin", **{"Plugin": plugin})
