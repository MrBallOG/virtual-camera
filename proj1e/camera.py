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
ANGLE_INCR2 = 1/180 * np.pi


class Camera:
    def __init__(self):
        self.point = np.mat(dtype=np.double, data=[0, 0, 10, 1]).T
        self.R = np.mat(dtype=np.int16, data=[[1, 0, 0, 0],
                                              [0, 1, 0, 0],
                                              [0, 0, 1, 0],
                                              [0, 0, 0, 1]])
        self.fov = 30
        self.scale = fov_to_scale(self.fov)

    def rotate_x_pos(self):
        self._rotate_x(1)

    def rotate_x_neg(self):
        self._rotate_x(-1)

    def rotate_y_pos(self):
        self._rotate_y(1)

    def rotate_y_neg(self):
        self._rotate_y(-1)

    def rotate_z_pos(self):
        self._rotate_z(1)

    def rotate_z_neg(self):
        self._rotate_z(-1)

    def _rotate_x(self, i):
        cos = np.cos(i * ANGLE_INCR2)
        sin = np.sin(i * ANGLE_INCR2)

        r_x = np.matrix(dtype=np.double, data=[[1, 0, 0, 0],
                                               [0, cos, sin, 0],
                                               [0, -sin, cos, 0],
                                               [0, 0, 0, 1]])
        self.R = r_x * self.R

    def _rotate_y(self, i):
        cos = np.cos(i * ANGLE_INCR2)
        sin = np.sin(i * ANGLE_INCR2)

        r_y = np.matrix(dtype=np.double, data=[[cos, 0, -sin, 0],
                                               [0, 1, 0, 0],
                                               [sin, 0, cos, 0],
                                               [0, 0, 0, 1]])

        self.R = r_y * self.R

    def _rotate_z(self, i):
        cos = np.cos(i * ANGLE_INCR2)
        sin = np.sin(i * ANGLE_INCR2)

        r_z = np.matrix(dtype=np.double, data=[[cos, sin, 0, 0],
                                               [-sin, cos, 0, 0],
                                               [0, 0, 1, 0],
                                               [0, 0, 0, 1]])
        self.R = r_z * self.R

    def rotate_point(self, point: np.matrix) -> np.matrix:
        point_at_origin = subtract_points(point, self.point)
        return self._rotate(point_at_origin)

    def _rotate(self, point: np.matrix) -> np.matrix:
        return self.R * point

    def _rotate2(self, point: np.matrix) -> np.matrix:
        rot = self.R.copy()
        rot_inv = np.linalg.inv(rot)

        return rot_inv * point

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
        rotated = self._rotate2(T_POINTS[:, i])
        self.point = add_points(self.point, rotated)

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
        rotated = self.rotate_point(point)
        temp = 1 / (1 - DIST)
        proj_mat = np.mat(dtype=np.double, data=[[self.scale, 0, 0, 0],
                                                 [0, self.scale, 0, 0],
                                                 [0, 0, temp, -DIST * temp],
                                                 [0, 0, 1, 0]])
        projected = proj_mat * rotated
        w = projected[3, 0]

        if w > 0.00000000000001:
            return None

        return (projected / w)[:2, 0]


def deg_to_rad(deg: int):
    return deg / 180 * np.pi


def add_points(p1: np.matrix, p2: np.matrix) -> np.matrix:
    return np.mat(dtype=np.double, data=[p1[0, 0] + p2[0, 0], p1[1, 0] + p2[1, 0], p1[2, 0] + p2[2, 0], 1]).T


def subtract_points(p1: np.matrix, p2: np.matrix, ) -> np.matrix:
    return np.mat(dtype=np.double, data=[p1[0, 0] - p2[0, 0], p1[1, 0] - p2[1, 0], p1[2, 0] - p2[2, 0], 1]).T


def fov_to_scale(fov: int) -> np.double:
    return 1 / np.tan(deg_to_rad(fov / 2))
