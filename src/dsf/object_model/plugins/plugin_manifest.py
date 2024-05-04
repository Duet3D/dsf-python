import re
from typing import List

from .sbc_permissions import SbcPermissions
from ..model_object import ModelObject


class PluginManifest(ModelObject):
    """Information about a third-party plugin"""
    
    def __init__(self):
        super(PluginManifest, self).__init__()
        self._author = None
        self._data = {}
        self._dwc_dependencies = []
        self._dwc_version = None
        self._homepage = None
        self._id = None
        self._license = "LGPL-3.0-or-later"
        self._name = None
        self._rrf_version = None
        self._sbc_auto_restart = False
        self._sbc_config_files = []
        self._sbc_dsf_version = None
        self._sbc_executable = None
        self._sbc_executable_arguments = []
        self._sbc_extra_executables = []
        self._sbc_output_redirected = None
        self._sbc_package_dependencies = []
        self._sbc_permissions = []  # Use a list instead of a set to keep insertion order (useful for json serialising)
        self._sbc_plugin_dependencies = []
        self._sbc_python_dependencies = []
        self._sbc_required = None
        self._tags = []
        self._version = "1.0.0"

    @property
    def author(self) -> str:
        """Author of the plugin"""
        return self._author

    @author.setter
    def author(self, value):
        self._author = str(value)

    @property
    def data(self):
        """Custom plugin data to be populated in the object model (DSF/DWC in SBC mode - or - DWC in standalone mode).
        Before Commands.SetPluginData can be used, corresponding properties must be registered via this property first!
        """
        return self._data

    @property
    def dwc_dependencies(self) -> List[str]:
        """List of DWC plugins this plugin depends on. Circular dependencies are not supported"""
        return self._dwc_dependencies

    @property
    def dwc_version(self) -> str:
        """Major/minor compatible DWC version"""
        return self._dwc_version

    @dwc_version.setter
    def dwc_version(self, value):
        self._dwc_version = str(value) if value is not None else None
        
    @property
    def homepage(self) -> str:
        """Link to the plugin homepage or source code repository"""
        return self._homepage
    
    @homepage.setter
    def homepage(self, value):
        self._homepage = str(value) if value is not None else None

    @property
    def id(self) -> str:
        """Identifier of this plugin. May consist of letters and digits only (max length 32 chars)
        For plugins with DWC components, this is the Webpack chunk name too"""
        return self._id

    @id.setter
    def id(self, value):
        if not value:
            raise Exception(f"Invalid plugin identifier: {value}")

        value = str(value)
        if value.isspace() or len(value) > 32:
            raise Exception(f"Invalid plugin identifier: {value}")
        for c in value:
            if not c.isalnum():
                raise Exception(f"Illegal plugin identifier: {value}")

        self._id = value

    @property
    def license(self) -> str:
        """License of the plugin. Should follow the SPDX format (see https://spdx.org/licenses/)"""
        return self._license

    @license.setter
    def license(self, value):
        self._license = str(value)

    @property
    def name(self) -> str:
        """Name of the plugin. May consist of letters, digits, dashes, and underscores only (max length 64 chars)"""
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise Exception(f"Invalid plugin name: {value}")

        value = str(value)
        if value.isspace() or len(value) > 64:
            raise Exception(f"Invalid plugin name: {value}")
        for c in value:
            if not c.isalnum() and c != ' ' and c != '-' and c != '_':
                raise Exception(f"Illegal plugin name: {value}")

        self._name = value

    @property
    def rrf_version(self) -> str:
        """Major/minor supported RRF version (optional)"""
        return self._rrf_version

    @rrf_version.setter
    def rrf_version(self, value):
        self._rrf_version = str(value) if value is not None else None

    @property
    def sbc_auto_restart(self) -> bool:
        """Automatically restart the SBC process when terminated"""
        return self._sbc_auto_restart

    @sbc_auto_restart.setter
    def sbc_auto_restart(self, value):
        self._sbc_auto_restart = bool(value)
        
    @property
    def sbc_config_files(self) -> List[str]:
        """List of files in the sys or virtual SD directory that should not be overwritten on upgrade
        The file may be specified either relative to 0:/sys directory (e.g. motion.conf) or relative to the
        virtual SD directory (e.g. sys/motion.conf). Drive indices as in 0:/sys/motion.conf are not allowed!"""
        return self._sbc_config_files

    @property
    def sbc_dsf_version(self) -> str:
        """Required DSF version for the plugin running on the SBC (ignored if there is no SBC executable)"""
        return self._sbc_dsf_version

    @sbc_dsf_version.setter
    def sbc_dsf_version(self, value):
        self._sbc_dsf_version = str(value) if value is not None else None

    @property
    def sbc_executable(self) -> str:
        """Filename in the dsf directory used to start the plugin
        A plugin may provide different binaries in subdirectories per architecture.
        Supported architectures are: arm, arm64, x86, x86_64"""
        return self._sbc_executable

    @sbc_executable.setter
    def sbc_executable(self, value):
        if value is not None:
            value = str(value)
            if '..' in value:
                raise Exception(f"Executable must not contain relative file paths: {value}")
        self._sbc_executable = value

    @property
    def sbc_executable_arguments(self) -> List[str]:
        """Command-line arguments for the executable"""
        return self._sbc_executable_arguments

    @sbc_executable_arguments.setter
    def sbc_executable_arguments(self, value):
        self._sbc_executable_arguments = str(value) if value is not None else None
        
    @property
    def sbc_extra_executables(self) -> List[str]:
        """List of other filenames in the dsf directory that should be executable"""
        return self._sbc_extra_executables

    @property
    def sbc_output_redirected(self) -> bool:
        """Defines if messages from stdout/stderr are output as generic messages"""
        return self._sbc_output_redirected
    
    @sbc_output_redirected.setter
    def sbc_output_redirected(self, value):
        self._sbc_output_redirected = bool(value)

    @property
    def sbc_package_dependencies(self) -> List[str]:
        """List of packages this plugin depends on (apt packages in the case of DuetPi)"""
        return self._sbc_package_dependencies
        
    @property
    def sbc_permissions(self) -> List[SbcPermissions]:
        """List of permissions required by the plugin executable running on the SBC"""
        return self._sbc_permissions
    
    @sbc_permissions.setter
    def sbc_permissions(self, values):
        permissions = []
        for value in values:
            if isinstance(value, SbcPermissions):
                permissions.append(value)
            elif isinstance(value, str):
                permissions.append(SbcPermissions(value))
            else:
                raise TypeError(f"{__name__}.sbc_permissions must be of type SbcPermissions."
                                f" Got {type(value)}: {value}")
        self._sbc_permissions = permissions
        
    @property
    def sbc_plugin_dependencies(self) -> List[str]:
        """List of SBC plugins this plugin depends on. Circular dependencies are not supported"""
        return self._sbc_plugin_dependencies
        
    @property
    def sbc_python_dependencies(self) -> List[str]:
        """List of Python packages this plugin depends on"""
        return self._sbc_python_dependencies

    @property
    def sbc_required(self) -> bool:
        """Set to true if an SBC is absolutely required for this plugin"""
        return self._sbc_required

    @sbc_required.setter
    def sbc_required(self, value):
        self._sbc_required = bool(value)
        
    @property
    def tags(self) -> List[str]:
        """List of general tags for search"""
        return self._tags

    @property
    def version(self) -> str:
        """Version of the plugin"""
        return self._version

    @version.setter
    def version(self, value):
        self._version = str(value)

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
