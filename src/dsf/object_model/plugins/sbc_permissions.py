from enum import IntEnum


class SbcPermissions(IntEnum):
    """Enumeration of supported plugin permissions"""

    # No permissions set (default value)
    noPermissions = 0

    # Execute generic commands
    commandExecution = 1

    # Intercept codes but don't interact with them
    codeInterceptionRead = 2

    # Intercept codes in a blocking way with options to resolve or cancel them
    codeInterceptionReadWrite = 4

    # Install, load, unload, and uninstall plugins. Grants FS access to all third-party plugins too
    managePlugins = 8

    # Service plugin runtime information (for internal purposes only, do not use)
    servicePlugins = 16

    # Manage user sessions
    manageUserSessions = 32

    # Read from the object model
    objectModelRead = 64

    # Read from and write to the object model
    objectModelReadWrite = 128

    # Create new HTTP endpoints
    registerHttpEndpoints = 256

    # Read files in 0:/filaments
    readFilaments = 512

    # Write files in 0:/filaments
    writeFilaments = 1024

    # Read files in 0:/firmware
    readFirmware = 2048

    # Write files in 0:/firmware
    writeFirmware = 4096

    # Read files in 0:/gcodes
    readGCodes = 8192

    # Write files in 0:/gcodes
    writeGCodes = 16384

    # Read files in 0:/macros
    readMacros = 32768

    # Write files in 0:/macros
    writeMacros = 65536

    # Read files in 0:/menu
    readMenu = 131072

    # Write files in 0:/menu
    writeMenu = 262144

    # Read files in 0:/sys
    readSystem = 524288

    # Write files in 0:/sys
    writeSystem = 1048576

    # Read files in 0:/www
    readWeb = 2097152

    # Write files in 0:/www
    writeWeb = 4194304

    # Access files including all subdirecotires of the virtual SD directory as DSF user
    fileSystemAccess = 8388608

    # Launch new processes
    launchProcesses = 16777216

    # Communicate over the network (stand-alone)
    networkAccess = 33554432

    # Access /dev/video* devices
    webcamAccess = 134217728

    # Access /dev/gpio*, /dev/i2c*, and /dev/spidev* devices
    gpioAccess = 268435456

    # Launch process as root user (for full device control - potentially dangerous)
    superUser = 67108864
