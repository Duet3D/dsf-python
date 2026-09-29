from datetime import datetime

from .cpu import CPU
from .memory import Memory
from .upgrade import Upgrade
from .dsf.dsf import DSF
from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class SBC(ModelObject):
    """Information about the SBC in SBC mode"""

    app_armor = model_prop('app_armor', bool, False)
    cpu = model_prop('cpu', CPU)
    dsf = model_prop('dsf', DSF)
    distribution = nullable_model_prop('distribution', str)
    distribution_build_time = nullable_model_prop('distribution_build_time', datetime, lambda: None)
    memory = model_prop('memory', Memory)
    model = nullable_model_prop('model', str)
    serial = nullable_model_prop('serial', str)
    upgrade = nullable_model_prop('upgrade', Upgrade)
    uptime = nullable_model_prop('uptime', float)

    def __init__(self):
        super().__init__()