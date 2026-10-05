from enum import IntFlag

from ..utils import DeprecatedAliasEnumType


class CodeFlags(IntFlag, metaclass=DeprecatedAliasEnumType):
    """Code bits to classify G/M/T-codes"""

    # Placeholder to indicate that no flags are set
    NONE = 0

    # Code execution finishes as soon as it is enqueued in the code queue
    # If codes are started asynchronously, code replies are normally reported via the object model.
    # In order to keep track of code replies, an <see cref="Connection.ConnectionMode.INTERCEPT"/> connection
    # in <see cref="Connection.InterceptionMode.EXECUTED"/> mode can be used
    ASYNCHRONOUS = 1

    # Code has been preprocessed (i.e. it has been processed by the DCS pre-side code interceptors)
    IS_PRE_PROCESSED = 2

    # Code has been postprocessed (i.e. it has been processed by the internal DCS code processor)
    IS_POST_PROCESSED = 4

    # Code originates from a macro file
    IS_FROM_MACRO = 8

    # Code originates from a system macro file (i.e. RRF requested it)
    IS_NESTED_MACRO = 16

    # Code comes from config.g or config.g.bak
    IS_FROM_CONFIG = 32

    # Code comes from config-override.g
    IS_FROM_CONFIG_OVERRIDE = 64

    # Enforce absolute positioning via prefixed G53 code
    ENFORCE_ABSOLUTE_POSITION = 128

    # Execute this code as quickly as possible and skip codes that have the <see cref="Unbuffered"/> flag set
    # In order to execute this code as quickly as possible, DCS attempts to change
    # the <see cref="Code.Channel"/> property to a code channel that is completely idle.
    # If this fails, a warning is logged. This flag should be only used for diagnostics and time-critical codes
    # like M112/M122/M999
    IS_PRIORITIZED = 256

    # Do NOT process another code on the same channel before this code has been fully executed.
    # Note that priority codes may still override codes that have this flag set
    UNBUFFERED = 512

    # Indicates if this code was requested from the firmware
    IS_FROM_FIRMWARE = 1024

    # Indicates if this is the last code on the line
    IS_LAST_CODE = 2048

    # Code has been processed internally (if this is set the internal execution of a code is skipped)
    IS_INTERNALLY_PROCESSED = 4096

    # Indicates if this code has an explicit line number (e.g. N1 G1 X10)
    HAS_EXPLICIT_LINE_NUMBER = 8192

    # Previous names, deprecated
    Asynchronous = ASYNCHRONOUS
    CodeFlagsNone = NONE
    EnforceAbsolutePosition = ENFORCE_ABSOLUTE_POSITION
    HasExplicitLineNumber = HAS_EXPLICIT_LINE_NUMBER
    IsFromConfig = IS_FROM_CONFIG
    IsFromConfigOverride = IS_FROM_CONFIG_OVERRIDE
    IsFromFirmware = IS_FROM_FIRMWARE
    IsFromMacro = IS_FROM_MACRO
    IsInternallyProcessed = IS_INTERNALLY_PROCESSED
    IsLastCode = IS_LAST_CODE
    IsNestedMacro = IS_NESTED_MACRO
    IsPostProcessed = IS_POST_PROCESSED
    IsPreProcessed = IS_PRE_PROCESSED
    IsPrioritized = IS_PRIORITIZED
    Unbuffered = UNBUFFERED
