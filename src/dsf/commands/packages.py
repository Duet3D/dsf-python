from .base_command import BaseCommand


def install_system_package(package_file: str):
    """Install or upgrade a system package
    :param package_file: Absolute file path to the package file
    """
    if not isinstance(package_file, str) or not package_file:
        raise TypeError("package_file must be a string")
    return BaseCommand("InstallSystemPackage", **{"PackageFile": package_file})


def uninstall_system_package(package: str):
    """Uninstall a system package
    :param package: Identifier of the package
    """
    if not isinstance(package, str) or not package:
        raise TypeError("package must be a string")
    return BaseCommand("UninstallSystemPackage", **{"Package": package})
