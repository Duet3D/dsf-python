#!/usr/bin/env python3

"""
Example of a command connection to send arbitrary commands to the machine

Make sure when running this script to have access to the DSF UNIX socket owned by the dsf user.
"""

from pydsfapi.connections import CommandConnection


def send_simple_code():
    command_connection = CommandConnection(debug=True)
    command_connection.connect()

    try:
        # Perform a simple command and wait for its output
        res = command_connection.perform_simple_code("M115")
        print("M115 is telling us:", res)
    finally:
        command_connection.close()


if __name__ == "__main__":
    send_simple_code()
