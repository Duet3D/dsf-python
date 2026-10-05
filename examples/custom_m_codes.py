#!/usr/bin/env python3

"""
Example of intercepting codes to implement custom M-codes

    M1234 S"name"   Reply with a greeting (S is optional)
    M1235 S"text"   Show a message on the display by running M117 on the same channel
    M1236           Stop this example

Try it by sending the codes above from the web interface console.

Make sure when running this script to have access to the DSF UNIX socket owned by the dsf user.
This is especially important when trying to run scripts as root user (which is not encouraged).
"""

from typing import Optional

from dsf.connections import InterceptConnection, InterceptionMode
from dsf.commands.code import Code, CodeType
from dsf.commands.code_parameter import CodeParameter
from dsf.object_model import MessageType


def start_intercept() -> None:
    # Only the filtered codes are sent to this connection, everything else is processed as usual.
    # InterceptionMode.PRE receives codes before DSF processes them. Use InterceptionMode.EXECUTED
    # instead to be notified about codes that have finished, e.g. to log them.
    # auto_flush (enabled by default) waits for all previous codes on the channel to finish first,
    # so this script is in sync with the machine whenever it receives a code
    filters: list[str] = ["M1234", "M1235", "M1236"]
    intercept_connection: InterceptConnection = InterceptConnection(InterceptionMode.PRE, filters=filters)
    intercept_connection.connect()

    try:
        while True:
            # Wait for a code to arrive
            code: Code = intercept_connection.receive_code()

            if code.type != CodeType.MCode:
                # Let DSF process codes we don't handle as if they were never intercepted
                intercept_connection.ignore_code()

            elif code.major_number == 1234:
                # Read a parameter, falling back to a default value if it is missing
                name: str = code.parameter("S", "world").string_value
                # Resolve the code with a reply so that DSF does not process it any further
                intercept_connection.resolve_code(MessageType.Success, f"Hello {name}!")

            elif code.major_number == 1235:
                text: Optional[CodeParameter] = code.parameter("S")
                if text is None:
                    intercept_connection.resolve_code(MessageType.Error, "Missing S parameter")
                    continue
                # Codes can be run while a code is intercepted. Use the channel of the intercepted
                # code so that they are executed in the same context
                intercept_connection.perform_simple_code(f'M117 "{text.string_value}"', code.channel)
                intercept_connection.resolve_code()

            elif code.major_number == 1236:
                intercept_connection.resolve_code(MessageType.Warning, "Custom M-code example stopped")
                return

            else:
                intercept_connection.ignore_code()
    finally:
        intercept_connection.close()


if __name__ == "__main__":
    start_intercept()
