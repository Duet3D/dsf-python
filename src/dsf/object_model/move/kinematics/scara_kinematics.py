from .zleadscrew_kinematics import ZLeadscrewKinematics


class ScaraKinematics(ZLeadscrewKinematics):
    """
    Kinematics class for SCARA kinematics
    """

    def __init__(self):
        super(ScaraKinematics, self).__init__()
