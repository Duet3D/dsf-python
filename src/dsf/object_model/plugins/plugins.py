from typing import List

from .plugin_manifest import PluginManifest


class Plugin(PluginManifest):
    """Class representing a loaded plugin"""

    def __init__(self):
        super(Plugin, self).__init__()
        self._dsf_files = []
        self._dwc_files = []
        self._sd_files = []
        self._pid = -1

    @property
    def dsf_files(self) -> List[str]:
        """List of files for the DSF plugin"""
        return self._dsf_files

    @property
    def dwc_files(self) -> List[str]:
        """List of files for the DWC plugin"""
        return self._dwc_files

    @property
    def sd_files(self) -> List[str]:
        """List of files to be installed to the (virtual) SD excluding web files"""
        return self._sd_files

    @property
    def pid(self) -> int:
        """Process ID of the plugin or -1 if not started. It is set to 0 while the plugin is being shut down"""
        return self._pid

    @pid.setter
    def pid(self, value):
        self._pid = int(value) if value is not None else -1

    def _update_from_json(self, **kwargs) -> 'Plugin':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(Plugin, self)._update_from_json(**kwargs)
        self._dsf_files = [str(item) for item in kwargs.get('dsfFiles', [])]
        self._dwc_files = [str(item) for item in kwargs.get('dwcFiles', [])]
        self._sd_files = [str(item) for item in kwargs.get('sdFiles', [])]
        return self
