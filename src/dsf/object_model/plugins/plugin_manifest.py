import re
from typing import List, Union

from .sbc_permissions import SbcPermissions
from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..model_dictionary import ModelDictionary
from ..utils import model_prop, nullable_model_prop


class PluginManifest(ModelObject):
    """Information about a third-party plugin"""

    # Identify of this plugin. May consist of letters and digits only (max length 32 chars)
    id = model_prop('id', str)

    # Name of the plugin. May consist of letters, digits, dashes, and underscores only (max length 64 chars)
    name = model_prop('name', str)

    # Author of the plugin
    author = model_prop('author', str, "")

    # Version of the plugin
    version = model_prop('version', str, "1.0.0")

    # Licence of the plugin. Should follow the SPDX format (see https://spdx.org/licenses/)
    license = model_prop('license', str, "LGPL-3.0-or-later")

    # Link to the plugin homepage or source code repository
    homepage = nullable_model_prop('homepage', str)

    # List of general tags for search
    tags = model_prop('tags', ModelCollection[str], ModelCollection(str))

    # Major/minor compatible DWC version
    dwc_version = nullable_model_prop('dwc_version', str)

    # List of DWC plugins this plugin depends on. Circular dependencies are not supported
    dwc_dependencies = model_prop('dwc_dependencies', ModelCollection[str], ModelCollection(str))

    # Set to true if a SBC is absolutely required for this plugin
    sbc_required = model_prop('sbc_required', bool)

    # Required DSF version for the plugin running on the SBC (ignored if there is no SBC executable)
    sbc_dsf_version = nullable_model_prop('sbc_dsf_version', str)

    # Filename in the dsf directory used to start the plugin
    sbc_executable = nullable_model_prop('sbc_executable', str)

    # Command-line arguments for the executable
    sbc_executable_arguments = nullable_model_prop('sbc_executable_arguments', str)

    # Automatically restart the SBC process when terminated
    sbc_auto_restart = model_prop('sbc_auto_restart', bool, False)
    
    # Plugin notifies DSF when it is fully started
    sbc_notify_started = model_prop('sbc_notify_started', bool, False)

    # Defines if messages from stdout/stderr are output as generic messages
    sbc_output_redirected = model_prop('sbc_output_redirected', bool, False)

    # List of permissins required by the plugin executable running on the SBC
    sbc_permissions = model_prop('sbc_permissions', ModelCollection[SbcPermissions], ModelCollection(SbcPermissions))

    # List of files in the sys or virtual SD directory that should not be overwritten on upgrade
    sbc_config_files = model_prop('sbc_config_files', ModelCollection[str], ModelCollection(str))

    # List of packages this plugin depends on (apt packages in the case of DuetPi)
    sbc_package_dependencies = model_prop('sbc_package_dependencies', ModelCollection[str], ModelCollection(str))

    # List of Python packages this plugin depends on
    sbc_python_dependencies = model_prop('sbc_python_dependencies', ModelCollection[str], ModelCollection(str))

    # List of SBC plugins this plugin depends on. Circular dependencies are not supported
    sbc_plugin_dependencies = model_prop('sbc_plugin_dependencies', ModelCollection[str], ModelCollection(str))

    # Major/minor compatible RRF version
    rrf_version = nullable_model_prop('rrf_version', str)

    # Custom plugin data to be populated in the object model (DSF/DWC in SBC mode - or - DWC in standalone mode).
    data = model_prop('data', ModelDictionary, ModelDictionary(False))
    
    def __init__(self):
        super(PluginManifest, self).__init__()

    @staticmethod
    def check_version(actual: str, required: str):
        """Check if the given version satisfies a required version
        :param actual: Actual version
        :param required: Required version
        :returns: Whether the actual version fulfills teh requirement"""
        split_chars = r'\.|-|\+'
        actual_items = re.split(split_chars, actual)
        required_items = re.split(split_chars, required)
        for actual_idx, required_idx in zip(actual_items, required_items):
            if actual_idx != required_idx:
                return False
        return True
