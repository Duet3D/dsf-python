from .kinematics_name import KinematicsName
from .zleadscrew_kinematics import ZLeadscrewKinematics


class CoreKinematics(ZLeadscrewKinematics):

    def __init__(self):
        super(CoreKinematics, self).__init__()
        self.name = KinematicsName.cartesian
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

    def _update_from_json(self, **kwargs) -> 'CoreKinematics':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(CoreKinematics, self)._update_from_json(**kwargs)
        self._forward_matrix = [[int(x) for x in y] for y in kwargs.get('forwardMatrix', [])]
        self._inverse_matrix = [[int(x) for x in y] for y in kwargs.get('inverseMatrix', [])]
        return self
