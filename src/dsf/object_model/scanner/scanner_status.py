from enum import Enum


class ScannerStatus(str, Enum):
    """Possible states of the attached 3D scanner"""

    # Scanner is disconnected (none present)
    disconnected = 'D'

    # Scanner is registered and idle
    idle = 'I'

    # Scanner is scanning an object
    scanning = 'S'

    # Scanner is post-processing a file
    postProcessing = 'P'

    # Scanner is calibrating
    calibrating = 'C'

    # Scanner is uploading
    uploading = 'U'
