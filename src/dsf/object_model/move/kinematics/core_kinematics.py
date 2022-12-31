from .kinematics_name import KinematicsName
from .zleadscrew_kinematics import ZLeadscrewKinematics


class CoreKinematics(ZLeadscrewKinematics):

    def __init__(self, name: KinematicsName = KinematicsName.cartesian):
        super(CoreKinematics, self).__init__(name)
        self._forward_matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        self._inverse_matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

    @property
    def forward_matrix(self):
        return self._forward_matrix

    @property
    def inverse_matrix(self):
        return self._inverse_matrix
