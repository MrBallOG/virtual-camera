import numpy as np


T_VAL = 0.1
T_POINTS = np.matrix(dtype=np.double, data=np.array([[T_VAL, 0, 0, 1],
                                                     [-T_VAL, 0, 0, 1],
                                                     [0, T_VAL, 0, 1],
                                                     [0, -T_VAL, 0, 1],
                                                     [0, 0, T_VAL, 1],
                                                     [0, 0, -T_VAL, 1]])).T
DIST = 0.1
ANGLE_INCR = 1


class Camera:
    def __init__(self, screen_scale: int, screen_center: np.matrix):
        self.point = np.mat(dtype=np.double, data=[0, 0, 10, 1]).T
        self.angle = np.mat(dtype=np.int16, data=[0, 0, 0]).T
        self.transform = self.get_transform()
        self.fov = 30
        self.scale = fov_to_scale(self.fov)
        self.screen_scale = screen_scale
        self.screen_center = screen_center

    def get_transform(self):
        phi, theta, psi = deg_to_rad(self.angle)
        cos_phi = np.cos(phi)
        sin_phi = np.sin(phi)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        cos_psi = np.cos(psi)
        sin_psi = np.sin(psi)

        r_x = np.matrix(dtype=np.double, data=[[1, 0, 0, 0],
                                               [0, cos_phi, sin_phi, 0],
                                               [0, -sin_phi, cos_phi, 0],
                                               [0, 0, 0, 1]])
        r_y = np.matrix(dtype=np.double, data=[[cos_theta, 0, -sin_theta, 0],
                                               [0, 1, 0, 0],
                                               [sin_theta, 0,
                                                cos_theta, 0],
                                               [0, 0, 0, 1]])

        r_z = np.matrix(dtype=np.double, data=[[cos_psi, sin_psi, 0, 0],
                                               [-sin_psi, cos_psi, 0, 0],
                                               [0, 0, 1, 0],
                                               [0, 0, 0, 1]])
        rot = r_x @ r_y @ r_z
        rot[:, 3] = self.point

        return rot

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
        self.angle[i, 0] += ANGLE_INCR
        self.transform = self.get_transform()

    def _rotate_neg(self, i: int):
        self.angle[i, 0] -= ANGLE_INCR
        self.transform = self.get_transform()

    def _rotate(self, point: np.matrix) -> np.matrix:
        return point

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
        rotated = self.transform @ T_POINTS[:, i]
        self.point = rotated
        self.transform[:, 3] = rotated

    def zoom_in(self):
        fov = self.fov
        if fov > 20:
            self.fov = fov - 10
            self.scale = fov_to_scale(self.fov)

    def zoom_out(self):
        fov = self.fov
        if fov < 100:
            self.fov = fov + 10
            self.scale = fov_to_scale(self.fov)

    def project_point(self, point: np.matrix) -> np.matrix:
        point = point3_to_point4(point)
        temp = 1 / (1 - DIST)
        proj_mat = np.mat(dtype=np.double, data=[[self.scale, 0, 0, 0],
                                                 [0, self.scale, 0, 0],
                                                 [0, 0, temp, -DIST * temp],
                                                 [0, 0, 1, 0]])
        projected = proj_mat @ self.transform @ point

        # return projected / projected[3, 0]
        return (projected / projected[3, 0])[:2, 0] * self.screen_scale + self.screen_center
        # z = projected[3, 0]

        # if z > 0.00000000000001:
        #     return None

        # return (projected / z)[:2, 0]


def deg_to_rad(deg: int):
    return deg / 180 * np.pi


def add_points(p1: np.matrix, p2: np.matrix) -> np.matrix:
    return np.mat(dtype=np.double, data=[p1[0, 0] + p2[0, 0], p1[1, 0] + p2[1, 0], p1[2, 0] + p2[2, 0], 1]).T


def subtract_points(p1: np.matrix, p2: np.matrix, ) -> np.matrix:
    return np.mat(dtype=np.double, data=[p1[0, 0] - p2[0, 0], p1[1, 0] - p2[1, 0], p1[2, 0] - p2[2, 0], 1]).T


def fov_to_scale(fov: int) -> np.double:
    return 1 / np.tan(deg_to_rad(fov / 2))


def point3_to_point4(p: np.matrix) -> np.matrix:
    return np.mat(dtype=np.double, data=[p[0, 0], p[1, 0], p[2, 0], 1]).T
