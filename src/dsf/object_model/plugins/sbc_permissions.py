from enum import Enum


class SbcPermissions(Enum):
    """Enumeration of supported plugin permissions"""

    # No permissions set (default value)
    noPermissions = "noPermissions"

    # Execute generic commands
    commandExecution = "commandExecution"

    # Intercept codes but don't interact with them
    codeInterceptionRead = "codeInterceptionRead"

    # Intercept codes in a blocking way with options to resolve or cancel them
    codeInterceptionReadWrite = "codeInterceptionReadWrite"

    # Install, load, unload, and uninstall plugins. Grants FS access to all third-party plugins too
    managePlugins = "managePlugins"

    # Service plugin runtime information (for internal purposes only, do not use)
    servicePlugins = "managePlugins"

    # Manage user sessions
    manageUserSessions = "manageUserSessions"

    # Read from the object model
    objectModelRead = "objectModelRead"

    # Read from and write to the object model
    objectModelReadWrite = "objectModelReadWrite"

    # Create new HTTP endpoints
    registerHttpEndpoints = "registerHttpEndpoints"

    # Read files in 0:/filaments
    readFilaments = "readFilaments"

    # Write files in 0:/filaments
    writeFilaments = "writeFilaments"

    # Read files in 0:/firmware
    readFirmware = "readFirmware"

    # Write files in 0:/firmware
    writeFirmware = "writeFirmware"

    # Read files in 0:/gcodes
    readGCodes = "readGCodes"

    # Write files in 0:/gcodes
    writeGCodes = "writeGCodes"

    # Read files in 0:/macros
    readMacros = "readMacros"

    # Write files in 0:/macros
    writeMacros = "writeMacros"

    # Read files in 0:/menu
    readMenu = "readMenu"

    # Write files in 0:/menu
    writeMenu = "writeMenu"

    # Read files in 0:/sys
    readSystem = "readSystem"

    # Write files in 0:/sys
    writeSystem = "writeSystem"

    # Read files in 0:/www
    readWeb = "readWeb"

    # Write files in 0:/www
    writeWeb = "writeWeb"

    # Access files including all subdirecotires of the virtual SD directory as DSF user
    fileSystemAccess = "fileSystemAccess"

    # Launch new processes
    launchProcesses = "launchProcesses"

    # Communicate over the network (stand-alone)
    networkAccess = "networkAccess"

    # Access /dev/video* devices
    webcamAccess = "webcamAccess"

    # Access /dev/gpio*, /dev/i2c*, and /dev/spidev* devices
    gpioAccess = "gpioAccess"

    # Launch process as root user (for full device control - potentially dangerous)
    superUser = "superUser"
