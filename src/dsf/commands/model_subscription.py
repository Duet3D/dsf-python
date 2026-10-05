from .base_command import BaseCommand


def acknowledge():
    """
    Acknowledge a (partial) model update.
    This command is only permitted in ConnectionMode.SUBSCRIBE mode.
    """
    return BaseCommand("Acknowledge")
