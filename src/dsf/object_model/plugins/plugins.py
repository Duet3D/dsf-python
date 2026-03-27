from .plugin_manifest import PluginManifest
from ..utils import model_prop
from ..model_collection import ModelCollection


class Plugin(PluginManifest):
    """Class representing a loaded plugin"""

    # List of files for the DSF plugin
    dsf_files = model_prop("dsf_files", ModelCollection[str], ModelCollection(str))

    # List of files for the DWC plugin
    dwc_files = model_prop("dwc_files", ModelCollection[str], ModelCollection(str))

    # List of files to be installed to the (virtual) SD excluding web files
    sd_files = model_prop("sd_files", ModelCollection[str], ModelCollection(str))

    # Process ID of the plugin or -1 if not started. It is set to 0 while the plugin is being shut down
    pid = model_prop("pid", int, -1)

    # Whether the plugin is started
    started = model_prop("started", bool, False)

    def __init__(self):
        super(Plugin, self).__init__()
