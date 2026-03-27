from .kinematics_name import KinematicsName
from .zleadscrew_kinematics import ZLeadscrewKinematics
from ...utils import model_prop
from ...model_collection import ModelCollection


class ScaraKinematics(ZLeadscrewKinematics):
    """
    Kinematics class for SCARA kinematics
    """

    # Proximal to distal, proximal to Z, and distal to Z crosstalk
    crosstalk = model_prop("crosstalk", ModelCollection[float], ModelCollection(float, [0.0, 0.0, 0.0]))

    # Distal arm length (in mm)
    distal_length = model_prop("distal_length", float, 0.0)

    # Requested minimum raidus (in mm)
    min_radius = model_prop("min_radius", float, 0.0)

    # Proximal arm length (in mm)
    proximal_length = model_prop("proximal_length", float, 0.0)

    # Psi limits (in degrees)
    psi_limits = model_prop("psi_limits", ModelCollection[float], ModelCollection(float, [0.0, 0.0]))

    # Theta limits (in degrees)
    theta_limits = model_prop("theta_limits", ModelCollection[float], ModelCollection(float, [0.0, 0.0]))

    # X offset (in mm)
    x_offset = model_prop("x_offset", float, 0.0)

    # Y offset (in mm)
    y_offset = model_prop("y_offset", float, 0.0)

    def __init__(self, name: KinematicsName):
        super(ScaraKinematics, self).__init__(name)

