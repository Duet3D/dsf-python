#!/usr/bin/env python3
"""
Example of intercepting and interacting with codes

Make sure when running this script to have access to the DSF UNIX socket owned by the dsf user.
This is especially important when trying to run scripts as root user (which is not encouraged).
"""

import subprocess
import traceback

from dsf.connections import InterceptConnection, InterceptionMode
from dsf.commands.code import CodeType
from dsf.object_model import MessageType


def start_intercept():
    # This demo script uses filters for the given three codes - M1234, M5678, M7722.
    # If you intercept the whole G-code stream (i.e. no filter) and if you wish to wait for all other
    # commands to be processed first, you MUST call flush() and wait for it to return true.
    # In the following M7722 section, the flush() call isn't required but it serves as a basic example
    filters = ["M1234", "M5678", "M7722"]
    intercept_connection = InterceptConnection(InterceptionMode.PRE, filters=filters, debug=True)
    intercept_connection.connect()

    try:
        while True:
            # Wait for a code to arrive
            cde = intercept_connection.receive_code()

            # Check for the type of the code
            if cde.type == CodeType.MCode and cde.majorNumber == 1234:
                # Do whatever needs to be done if this is the right code
                print(cde, cde.flags)

                # Resolve it so that DCS knows we took care of it
                intercept_connection.resolve_code()
            elif cde.type == CodeType.MCode and cde.majorNumber == 5678:
                intercept_connection.resolve_code()
                intercept_connection.close()
                # Exit this example
                return
            elif cde.type == CodeType.MCode and cde.majorNumber == 7722:
                # --------------- BEGIN FLUSH ---------------------
                # Flushing is necessary if the action below needs to be in sync with the machine
                # at this point in the GCode stream. If you only wish to inspect or log the G-code(s),
                # it is not needed. It is not needed either if a filter is set, see above

                # Flush the code's channel to be sure we are being in sync with the machine
                success = intercept_connection.flush(cde.channel)

                # Flushing failed so we need to cancel our code
                if not success:
                    print("Flush failed")
                    intercept_connection.cancel_code()
                    continue
                # -------------- END FLUSH ------------------------

                # We are going to shut down the SBC in one minute
                subprocess.run(["sudo", "shutdown", "+1"])
                # Resolve it with a custom response message text
                intercept_connection.resolve_code(MessageType.Warning, "Shutting down SBC in 1min...")
            else:
                # We did not handle it so we ignore it and it will be continued to be processed
                intercept_connection.ignore_code()
    except Exception as e:
        print("Closing connection: ", e)
        traceback.print_exc()
        intercept_connection.close()


if __name__ == "__main__":
    start_intercept()
