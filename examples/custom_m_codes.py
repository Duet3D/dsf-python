#!/usr/bin/env python3
"""
Example of intercepting and interacting with codes

Make sure when running this script to have access to the DSF UNIX socket owned by the dsf user.
"""

import subprocess
import traceback

from dsf.connections import InterceptConnection, InterceptionMode
from dsf.commands.code import CodeType
from dsf.object_model import MessageType

# needed to resolve meta variables
from dsf.connections import CommandConnection
from dsf.commands.generic import evaluate_expression


# function to ask RRF to resolve a meta variable
def eval_expr( meta_var, channel):
    command_connection = CommandConnection(debug=True)
    command_connection.connect()

    try:
        res = command_connection.perform_command(evaluate_expression( channel, meta_var ))
        result = res.result
        print(f"Evaluated expression: {result}")
    finally:
        command_connection.close()

    return result


def start_intercept():
    filters = ["M1234", "M5678", "M7722"]
    intercept_connection = InterceptConnection(InterceptionMode.PRE, filters=filters, debug=True)
    intercept_connection.connect()

    try:
        while True:
            # Wait for a code to arrive
            cde = intercept_connection.receive_code()

            # Check for the type of the code
            if cde.type == CodeType.MCode and cde.majorNumber == 1234:
                # --------------- BEGIN FLUSH ---------------------
                # Flushing is only necessary if the action below needs to be in sync with the machine
                # at this point in the GCode stream. Otherwise, it can and should be skipped

                # Flush the code's channel to be sure we are being in sync with the machine
                success = intercept_connection.flush(cde.channel)

                # Flushing failed so we need to cancel our code
                if not success:
                    print("Flush failed")
                    intercept_connection.cancel_code()
                    continue
                # -------------- END FLUSH ------------------------

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
                if cde.parameter("S") is None :
                    # if there isnt an S parameter set minutes to 1
                    minutes = "1"
                elif cde.parameter("S").is_expression :
                    # if there is an S parameter and it is an expression 
                    # resolve the expression and set minutes equal to it
                    minutes = eval_expr( cde.parameter("S").string_value, cde.channel )
                else :
                    # if there is an S parameter and it isnt an expression
                    # set minutes to it
                    minutes = cde.parameter("S").string_value

                # add a + to the beginning of minutes
                min_plus = "+" + str(minutes)

                # We are going to shut down the SBC in one minute
                subprocess.run(["sudo", "shutdown", min_plus])

                # Resolve it with a custom response message text
                warn_msg = "Shutting down SBC in " + str(minutes) + "min..."
                intercept_connection.resolve_code(MessageType.Warning, warn_msg)
            else:
                # We did not handle it so we ignore it and it will be continued to be processed
                intercept_connection.ignore_code()
    except Exception as e:
        print("Closing connection: ", e)
        traceback.print_exc()
        intercept_connection.close()


if __name__ == "__main__":
    start_intercept()
