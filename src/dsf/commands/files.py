from .base_command import BaseCommand


def get_file_info(file_name: str, read_thumbnail_content: bool = False):
    """
    Analyse a G-code file and return an instance of GetFileInfo when ready
    :param file_name: The filename to extract information from
    :param read_thumbnail_content: Whether thumbnail content shall be returned
    """
    if not isinstance(file_name, str) or not file_name:
        raise TypeError("file_name must be a string")
    return BaseCommand("GetFileInfo", **{"fileName": file_name, "readThumbnailContent": read_thumbnail_content})


def resolve_path(path: str, base_directory: str = None):
    """
    Resolve a RepRapFirmware-style path to an actual file path
    :param path: Path that is RepRapFirmware-compatible
    :param base_directory: Optional base directory to resolve the path relative to
    :returns: The resolved path
    """
    if not isinstance(path, str) or not path:
        raise TypeError("path must be a string")
    return BaseCommand("ResolvePath", **{"path": path, "baseDirectory": base_directory})
