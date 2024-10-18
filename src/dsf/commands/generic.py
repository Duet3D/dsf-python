from typing import Optional

from .base_command import BaseCommand
from .code_channel import CodeChannel
from ..object_model.state.log_level import LogLevel
from ..object_model.messages import MessageType


def check_password(password: str):
    """
    Check if the given password is correct and matches the previously set value from M551.
    If no password was configured before or if it was set to "reprap", this will always return true

    :param password: Password to check

    :returns: true if the password matches or is not set
    """
    if not isinstance(password, str) or not password:
        raise TypeError("password must be a string")
    return BaseCommand("CheckPassword", **{"password": password})


def evaluate_expression(channel: CodeChannel, expression: str):
    """
    Evaluate an arbitrary expression on the given channel in RepRapFirmware.
    Do not use this call to evaluate file-based and network-related fields because the
    DSF and RRF models diverge in this regard.

    :param channel: Code channel where the expression is evaluated
    :param expression: Expression to evaluate
    """
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    if not isinstance(expression, str) or not expression:
        raise TypeError("expression must be a string")
    return BaseCommand("EvaluateExpression", **{"channel": channel, "expression": expression})


def flush(channel: CodeChannel, sync_file_streams: bool = False, if_executing: bool = True):
    """
    Wait for all pending (macro) codes on the given channel to finish.
    This effectively guarantees that all buffered codes are processed by RRF before this command finishes.

    :param channel: Code channel to flush
    :param sync_file_streams: Whether the File and File2 streams are supposed to synchronize if a code is being
    intercepted. This option should be used with care, under certain circumstances this can lead to a deadlock!
    :param if_executing: Check if the corresponding channel is actually executing codes (i.e. if it is active).
    If the input channel is not active, this command returns false.
    This option is ignored if SyncFileStreams is true.

    :returns: true if the flush request is successful
    """
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    if not isinstance(sync_file_streams, bool):
        raise TypeError("sync_file_streams must be a boolean")
    if not isinstance(if_executing, bool):
        raise TypeError("if_executing must be a boolean")
    return BaseCommand("Flush",
                       **{"channel": channel, "syncFileStreams": sync_file_streams, "ifExecuting": if_executing})


def invalidate_channel(channel: CodeChannel):
    """
    Invalidate all pending codes and files on a given channel (including buffered codes from DSF in RepRapFirmware)

    :param channel: Code channel to invalidate

    :returns: true if the invalidate request is successful
    """
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    return BaseCommand("InvalidateChannel", **{"channel": channel})


def set_update_status(updating: bool):
    """
    Override the current status as reported by the object model when performing a software update.

    :param updating: Whether an update is now in progress
    """
    if not isinstance(updating, bool):
        raise TypeError("updating must be a boolean")
    return BaseCommand("SetUpdateStatus", **{"updating": updating})


def simple_code(code: str, channel: CodeChannel = CodeChannel.DEFAULT_CHANNEL, async_exec: bool = False):
    """
    Perform a simple G/M/T-code
    Internally the code passed is populated as a full Code instance and on completion
    its Code.Result is transformed back into a basic string. This is useful for minimal
    extensions that do not require granular control of the code details. Except for certain cases, it
    is NOT recommended for usage in InterceptionMode because it renders the internal code buffer useless.

    :param code: Code to parse and execute
    :param channel: Destination channel
    :param async_exec: Whether this code may be executed asynchronously.
                       If set, the code reply is output as a generic message
    """
    if not isinstance(code, str) or not code:
        raise TypeError("code must be a string")
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    return BaseCommand("SimpleCode", **{"code": code, "channel": channel, "executeAsynchronously": async_exec})


def write_message(
    message_type: MessageType,
    content: str,
    output_message: bool = True,
    log_level: Optional[LogLevel] = None,
):
    """
    Write an arbitrary generic message

    :param message_type: Type of the message to write
    :param content: Content of the message to write
    :param output_message: Output the message on the console and via the object model
    :param log_level: Log level of this message
    """
    if not isinstance(message_type, MessageType):
        raise TypeError("rtype must be a MessageType")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(output_message, bool):
        raise TypeError("output_message must be a boolean")
    if log_level is not None and not isinstance(log_level, LogLevel):
        raise TypeError("log_message must be a LogLevel")
    return BaseCommand(
        "WriteMessage",
        **{
            "type": message_type,
            "content": content,
            "outputMessage": output_message,
            "logLevel": log_level,
        },
    )
