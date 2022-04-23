import numpy as np


class Camera:
    def __init__(self):
        self.point4 = np.mat(dtype=np.double, data=[0, 0, 0, 1]).T
        self.angle = np.mat(dtype=np.int16, data=[0, 0, 0]).T
        self.q = self._euler_to_quaternion()

    def rotate_x_pos(self):
        self._rotate_pos(0)

    def rotate_x_neg(self):
        self._rotate_neg(0)

    def rotate_y_pos(self):
        self._rotate_pos(1)

    def rotate_y_neg(self):
        self._rotate_neg(1)

    def rotate_z_pos(self):
        self._rotate_pos(2)

    def rotate_z_neg(self):
        self._rotate_neg(2)

    def _rotate_pos(self, i):
        current = self.angle[i, 0]
        self.angle[i, 0] = current + 5 if current < 355 else 0
        self.q = self._euler_to_quaternion()

    def _rotate_neg(self, i):
        current = self.angle[i, 0]
        self.angle[i, 0] = current - 5 if current > 0 else 355
        self.q = self._euler_to_quaternion()

    def _euler_to_quaternion(self):
        phi = deg_to_rad(self.angle[0, 0])
        theta = deg_to_rad(self.angle[1, 0])
        psi = deg_to_rad(self.angle[2, 0])

        cos_phi = np.cos(phi/2)
        sin_phi = np.sin(phi/2)
        cos_theta = np.cos(theta/2)
        sin_theta = np.sin(theta/2)
        cos_psi = np.cos(psi/2)
        sin_psi = np.sin(psi/2)

        w = cos_phi * cos_theta * cos_psi + sin_phi * sin_theta * sin_psi
        x = sin_phi * cos_theta * cos_psi - cos_phi * sin_theta * sin_psi
        y = cos_phi * sin_theta * cos_psi + sin_phi * cos_theta * sin_psi
        z = cos_phi * cos_theta * sin_psi - sin_phi * sin_theta * cos_psi

        return np.mat(dtype=np.double, data=[w, x, y, z]).T


def deg_to_rad(deg: int):
    return deg / 180 * np.pi
