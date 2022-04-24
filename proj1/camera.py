import numpy as np


T_VAL = 0.2
T_POINTS = np.matrix(dtype=np.double, data=np.array([[T_VAL, 0, 0, 1],
                                                     [-T_VAL, 0, 0, 1],
                                                     [0, T_VAL, 0, 1],
                                                     [0, -T_VAL, 0, 1],
                                                     [0, 0, T_VAL, 1],
                                                     [0, 0, -T_VAL, 1]])).T
DIST = 0.5


class Camera:
    def __init__(self):
        self.point = np.mat(dtype=np.double, data=[0, 0, 0, 1]).T
        self.angle = np.mat(dtype=np.int16, data=[0, 0, 0]).T
        self.q = self._euler_to_quaternion()
        self.q_con = self._quaternion_conjugate()
        self.fov = 90
        self.scale = fov_to_scale(self.fov)

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

    def _rotate_pos(self, i: int):
        current = self.angle[i, 0]
        self.angle[i, 0] = current + 5 if current < 355 else 0
        self.q = self._euler_to_quaternion()
        self.q_con = self._quaternion_conjugate()

    def _rotate_neg(self, i: int):
        current = self.angle[i, 0]
        self.angle[i, 0] = current - 5 if current > 0 else 355
        self.q = self._euler_to_quaternion()
        self.q_con = self._quaternion_conjugate()

    def _euler_to_quaternion(self) -> np.matrix:
        phi, theta, psi = deg_to_rad(self.angle)

        cos_phi = np.cos(phi / 2)
        sin_phi = np.sin(phi / 2)
        cos_theta = np.cos(theta / 2)
        sin_theta = np.sin(theta / 2)
        cos_psi = np.cos(psi / 2)
        sin_psi = np.sin(psi / 2)

        w = cos_phi * cos_theta * cos_psi + sin_phi * sin_theta * sin_psi
        x = sin_phi * cos_theta * cos_psi - cos_phi * sin_theta * sin_psi
        y = cos_phi * sin_theta * cos_psi + sin_phi * cos_theta * sin_psi
        z = cos_phi * cos_theta * sin_psi - sin_phi * sin_theta * cos_psi

        return np.mat(dtype=np.double, data=[w[0, 0], x[0, 0], y[0, 0], z[0, 0]]).T

    def _quaternion_conjugate(self) -> np.matrix:
        return np.mat(dtype=np.double, data=[self.q[0, 0], -self.q[1, 0], -self.q[2, 0], -self.q[3, 0]]).T

    def rotate_point(self, point: np.matrix) -> np.matrix:
        point_at_origin = subtract_points(point, self.point)
        rotated = self._rotate(point_at_origin)

        # return add_points(np.mat(dtype=np.double, data=[rotated[1, 0], rotated[2, 0], rotated[3, 0], 1]).T, self.point)
        return np.mat(dtype=np.double, data=[rotated[1, 0], rotated[2, 0], rotated[3, 0], 1]).T

    def _rotate(self, point: np.matrix) -> np.matrix:
        q_p = np.mat(dtype=np.double, data=[
                     0, point[0, 0], point[1, 0], point[2, 0]]).T
        return hamilton_product(hamilton_product(self.q, q_p), self.q_con)

    def translate_x_pos(self):
        self._translate(0)

    def translate_x_neg(self):
        self._translate(1)

    def translate_y_pos(self):
        self._translate(2)

    def translate_y_neg(self):
        self._translate(3)

    def translate_z_pos(self):
        self._translate(4)

    def translate_z_neg(self):
        self._translate(5)

    def _translate(self, i: int):
        rotated = self._rotate(T_POINTS[:, i])
        self.point = add_points(self.point, np.mat(dtype=np.double, data=[
                                rotated[1, 0], rotated[2, 0], rotated[3, 0], 1]).T)

    def zoom_in(self):
        fov = self.fov
        if fov > 30:
            self.fov = fov - 30
            self.scale = fov_to_scale(self.fov)

    def zoom_out(self):
        fov = self.fov
        if fov < 150:
            self.fov = fov + 30
            self.scale = fov_to_scale(self.fov)

    def project_point(self, point: np.matrix) -> np.matrix:
        rotated = self.rotate_point(point)
        temp = 1 / (1 - DIST)
        proj_mat = np.mat(dtype=np.double, data=[[self.scale, 0, 0, 0],
                                                 [0, self.scale, 0, 0],
                                                 [0, 0, temp, -DIST * temp],
                                                 [0, 0, 1, 0]])
        projected = proj_mat @ rotated

        return (projected / projected[2, 0])[:2, 0]


def deg_to_rad(deg: int):
    return deg / 180 * np.pi


def hamilton_product(q1: np.matrix, q2: np.matrix):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2

    return np.mat(dtype=np.double, data=[w[0, 0], x[0, 0], y[0, 0], z[0, 0]]).T


def add_points(p1: np.matrix, p2: np.matrix) -> np.matrix:
    return np.mat(dtype=np.double, data=[p1[0, 0] + p2[0, 0], p1[1, 0] + p2[1, 0], p1[2, 0] + p2[2, 0], 1]).T


def subtract_points(p1: np.matrix, p2: np.matrix, ) -> np.matrix:
    return np.mat(dtype=np.double, data=[p1[0, 0] - p2[0, 0], p1[1, 0] - p2[1, 0], p1[2, 0] - p2[2, 0], 1]).T


def fov_to_scale(fov: int) -> np.double:
    return 1 / np.tan(deg_to_rad(fov / 2))
