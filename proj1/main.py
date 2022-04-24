from camera import Camera, deg_to_rad, hamilton_product, T_POINTS
import numpy as np


def main():
    cam = Camera()

    l = [90, 45, 90]
    for i in range(3):
        cam.angle[i, 0] = l[i]

    q = cam._euler_to_quaternion()
    cam.q = q
    cam.q_con = cam._quaternion_conjugate()
    print(q)

    v = np.mat(dtype=np.double, data=[1, 0, 0, 1]).T
    print(v)

    cam.point[0, 0] = 3
    cam.point[1, 0] = 5
    cam.point[2, 0] = 15
    v2 = cam.rotate_point(v)
    print(cam.point)
    cam.translate_x_pos()
    print(np.round(v2, decimals=2))

    print(cam.point)

    # x, y, z = deg_to_rad(cam.angle)
    # print(x[0, 0])
    # x, y, z = cam.angle
    # print(deg_to_rad(x))
    # print(hamilton_product(cam.q, cam.q))

    # should_render = True

    # while True:
    #     # key check
    #     if should_render:
    #         # do some
    #         should_render = False


main()
