from .base_command import BaseCommand


def install_plugin(plugin_file: str):
    """
    Install or upgrade a plugin
    :param plugin_file: Absolute file path to the plugin ZIP bundle
    """
    if not isinstance(plugin_file, str) or not plugin_file:
        raise TypeError("plugin_file must be a string")
    return BaseCommand("InstallPlugin", **{"PluginFile": plugin_file})


def reload_plugin(plugin: str):
    """
    Reload the manifest of a given plugin. Useful for packaged plugins
    :param plugin: Identifier of the plugin
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("ReloadPlugin", **{"Plugin": plugin})


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


def start_plugin(plugin: str, save_state: bool = True):
    """
    Start a plugin
    :param plugin: Identifier of the plugin
    :param save_state: Defines if the list of executing plugins may be saved
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("StartPlugin", **{"Plugin": plugin, "SaveState": save_state})


def start_plugins():
    """Start all the previously started plugins again"""
    return BaseCommand("StartPlugins")


def stop_plugin(plugin: str, save_state: bool = True):
    """
    Stop a plugin
    :param plugin: Identifier of the plugin
    :param save_state: Defines if the list of executing plugins may be saved
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("StopPlugin", **{"Plugin": plugin, "SaveState": save_state})


def stop_plugins():
    """Stop all the plugins and save which plugins were started before.
    This command is intended for shutdown or update requests"""
    return BaseCommand("StopPlugins")


def uninstall_plugin(plugin: str):
    """
    Uninstall a plugin
    :param plugin: Identifier of the plugin
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("UninstallPlugin", **{"Plugin": plugin})
