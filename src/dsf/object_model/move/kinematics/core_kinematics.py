from .kinematics_name import KinematicsName
from .zleadscrew_kinematics import ZLeadscrewKinematics
from ...utils import model_prop


class CoreKinematics(ZLeadscrewKinematics):

    forward_matrix = model_prop("forward_matrix", list[list[float]], [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
    inverse_matrix = model_prop("inverse_matrix", list[list[float]], [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])

    def __init__(self, name: KinematicsName = KinematicsName.cartesian):
        super(CoreKinematics, self).__init__(name)
