from enum import IntEnum


class CodeFlags(IntEnum):
    """Code bits to classify G/M/T-codes"""

    # Placeholder to indicate that no flags are set
    CodeFlagsNone = 0

    # Code execution finishes as soon as it is enqueued in the code queue
    # If codes are started asynchronously, code replies are normally reported via the object model.
    # In order to keep track of code replies, an <see cref="Connection.ConnectionMode.Intercept"/> connection
    # in <see cref="Connection.InterceptionMode.Executed"/> mode can be used
    Asynchronous = 1

    # Code has been preprocessed (i.e. it has been processed by the DCS pre-side code interceptors)
    IsPreProcessed = 2

    # Code has been postprocessed (i.e. it has been processed by the internal DCS code processor)
    IsPostProcessed = 4

    # Code originates from a macro file
    IsFromMacro = 8

    # Code originates from a system macro file (i.e. RRF requested it)
    IsNestedMacro = 16

    # Code comes from config.g or config.g.bak
    IsFromConfig = 32

    # Code comes from config-override.g
    IsFromConfigOverride = 64

    # Enforce absolute positioning via prefixed G53 code
    EnforceAbsolutePosition = 128

    # Execute this code as quickly as possible and skip codes that have the <see cref="Unbuffered"/> flag set
    # In order to execute this code as quickly as possible, DCS attempts to change
    # the <see cref="Code.Channel"/> property to a code channel that is completely idle.
    # If this fails, a warning is logged. This flag should be only used for diagnostics and time-critical codes
    # like M112/M122/M999
    IsPrioritized = 256

    # Do NOT process another code on the same channel before this code has been fully executed.
    # Note that priority codes may still override codes that have this flag set
    Unbuffered = 512

    # Indicates if this code was requested from the firmware
    IsFromFirmware = 1024

    # Indicates if this is the last code on the line
    IsLastCode = 2048

    # Code has been processed internally (if this is set the internal execution of a code is skipped)
    IsInternallyProcessed = 4096
