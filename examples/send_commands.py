#!/usr/bin/env python3

"""
Example of a command connection to run codes and query the machine

Make sure when running this script to have access to the DSF UNIX socket owned by the dsf user.
"""

from dsf.connections import CommandConnection, InternalServerException
from dsf.object_model import LogLevel, MessageType, ObjectModel


def send_commands() -> None:
    command_connection: CommandConnection = CommandConnection()
    command_connection.connect()

    try:
        # Run a G/M/T-code and wait for its reply
        reply: str = command_connection.perform_simple_code("M115")
        print("M115 is telling us:", reply.strip())

        # Evaluate a meta G-code expression without running a code.
        # The result can be any JSON value depending on the expression
        up_time = command_connection.evaluate_expression("state.upTime").result
        print(f"Machine has been up for {up_time}s")

        # Get parts of the object model as typed Python objects.
        # Leave out the filters to get the whole object model
        object_model: ObjectModel = command_connection.get_object_model(["state", "move.axes"])
        print("Machine status:", object_model.state.status.value)
        for axis in object_model.move.axes:
            print(f"Axis {axis.letter.value}: {axis.min} to {axis.max}mm, homed: {axis.homed}")

        # Show a message in the web interface and write it to the log file
        command_connection.write_message(MessageType.Success, "Hello from dsf-python!", True, LogLevel.Info)

        # Errors reported by DSF are raised as exceptions
        try:
            command_connection.evaluate_expression("does.not.exist")
        except InternalServerException as e:
            print(f"DSF returned an error: {e.error_type}: {e.error_message}")
    finally:
        command_connection.close()


if __name__ == "__main__":
    send_commands()
