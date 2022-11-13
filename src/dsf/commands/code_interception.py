from typing import Optional

from .base_command import BaseCommand
from ..object_model.messages import MessageType


def cancel():
    """Cancel a code in Connection.InterceptionMode."""
    return BaseCommand("Cancel")


def ignore():
    """
    Ignore the code to intercept and allow it to be processed without any modifications.
    This command is only permitted in ConnectionMode.Intercept mode.
    """
    return BaseCommand("Ignore")


def resolve_code(rtype: MessageType, content: Optional[str]):
    """
    Resolve the code to intercept and return the given message details for its completion.
    This command is only permitted in ConnectionMode.Intercept mode.
    :param rtype: Type of the resolving message
    :param content: Content of the resolving message
    """
    if not isinstance(rtype, MessageType):
        raise TypeError("rtype must be a MessageType")
    if content is not None and not isinstance(content, str):
        raise TypeError("content must be None or a string")
    return BaseCommand("Resolve", **{"Type": rtype, "Content": content})
