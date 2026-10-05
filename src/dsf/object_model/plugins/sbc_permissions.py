from enum import Enum

from ...utils import DeprecatedAliasEnumType


class SbcPermissions(Enum, metaclass=DeprecatedAliasEnumType):
    """Enumeration of supported plugin permissions"""

    # No permissions set (default value)
    NONE = "none"

    # Execute generic commands
    COMMAND_EXECUTION = "commandExecution"

    # Intercept codes but don't interact with them
    CODE_INTERCEPTION_READ = "codeInterceptionRead"

    # Intercept codes in a blocking way with options to resolve or cancel them
    CODE_INTERCEPTION_READ_WRITE = "codeInterceptionReadWrite"

    # Install, load, unload, and uninstall plugins. Grants FS access to all third-party plugins too
    MANAGE_PLUGINS = "managePlugins"

    # Service plugin runtime information (for internal purposes only, do not use)
    SERVICE_PLUGINS = "servicePlugins"

    # Manage user sessions
    MANAGE_USER_SESSIONS = "manageUserSessions"

    # Read from the object model
    OBJECT_MODEL_READ = "objectModelRead"

    # Read from and write to the object model
    OBJECT_MODEL_READ_WRITE = "objectModelReadWrite"

    # Create new HTTP endpoints
    REGISTER_HTTP_ENDPOINTS = "registerHttpEndpoints"

    # Read files in 0:/filaments
    READ_FILAMENTS = "readFilaments"

    # Write files in 0:/filaments
    WRITE_FILAMENTS = "writeFilaments"

    # Read files in 0:/firmware
    READ_FIRMWARE = "readFirmware"

    # Write files in 0:/firmware
    WRITE_FIRMWARE = "writeFirmware"

    # Read files in 0:/gcodes
    READ_GCODES = "readGCodes"

    # Write files in 0:/gcodes
    WRITE_GCODES = "writeGCodes"

    # Read files in 0:/macros
    READ_MACROS = "readMacros"

    # Write files in 0:/macros
    WRITE_MACROS = "writeMacros"

    # Read files in 0:/menu
    READ_MENU = "readMenu"

    # Write files in 0:/menu
    WRITE_MENU = "writeMenu"

    # Read files in 0:/sys
    READ_SYSTEM = "readSystem"

    # Write files in 0:/sys
    WRITE_SYSTEM = "writeSystem"

    # Read files in 0:/www
    READ_WEB = "readWeb"

    # Write files in 0:/www
    WRITE_WEB = "writeWeb"

    # Access files including all subdirecotires of the virtual SD directory as DSF user
    FILE_SYSTEM_ACCESS = "fileSystemAccess"

    # Launch new processes
    LAUNCH_PROCESSES = "launchProcesses"

    # Communicate over the network (stand-alone)
    NETWORK_ACCESS = "networkAccess"

    # Access /dev/video* devices
    WEBCAM_ACCESS = "webcamAccess"

    # Access /dev/gpio*, /dev/i2c*, and /dev/spidev* devices
    GPIO_ACCESS = "gpioAccess"

    # Launch process as root user (for full device control - potentially dangerous)
    SUPER_USER = "superUser"

    # Previous names, deprecated
    codeInterceptionRead = CODE_INTERCEPTION_READ
    codeInterceptionReadWrite = CODE_INTERCEPTION_READ_WRITE
    commandExecution = COMMAND_EXECUTION
    fileSystemAccess = FILE_SYSTEM_ACCESS
    gpioAccess = GPIO_ACCESS
    launchProcesses = LAUNCH_PROCESSES
    managePlugins = MANAGE_PLUGINS
    manageUserSessions = MANAGE_USER_SESSIONS
    networkAccess = NETWORK_ACCESS
    noPermissions = NONE
    objectModelRead = OBJECT_MODEL_READ
    objectModelReadWrite = OBJECT_MODEL_READ_WRITE
    readFilaments = READ_FILAMENTS
    readFirmware = READ_FIRMWARE
    readGCodes = READ_GCODES
    readMacros = READ_MACROS
    readMenu = READ_MENU
    readSystem = READ_SYSTEM
    readWeb = READ_WEB
    registerHttpEndpoints = REGISTER_HTTP_ENDPOINTS
    servicePlugins = SERVICE_PLUGINS
    superUser = SUPER_USER
    webcamAccess = WEBCAM_ACCESS
    writeFilaments = WRITE_FILAMENTS
    writeFirmware = WRITE_FIRMWARE
    writeGCodes = WRITE_GCODES
    writeMacros = WRITE_MACROS
    writeMenu = WRITE_MENU
    writeSystem = WRITE_SYSTEM
    writeWeb = WRITE_WEB
