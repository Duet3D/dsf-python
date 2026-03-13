from .base_command import BaseCommand


def install_system_package(package_file: str):
    """Install or upgrade a system package
    :param package_file: Absolute file path to the package file
    """
    if not package_file:
        raise ValueError("package_file must not be empty")
    return BaseCommand("InstallSystemPackage", **{"packageFile": package_file})


def uninstall_system_package(package: str):
    """Uninstall a system package
    :param package: Identifier of the package
    """
    if not package:
        raise ValueError("package must not be empty")
    return BaseCommand("UninstallSystemPackage", **{"package": package})
