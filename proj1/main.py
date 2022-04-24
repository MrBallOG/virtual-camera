from camera import Camera, deg_to_rad, hamilton_product, T_POINTS
import numpy as np
import pygame as pg


def main():
    width, height = 1000, 800
    black = (30, 30, 30)
    white = (255, 255, 255)
    yellow = (249, 215, 28)

    cam = Camera()
    pg.init()
    pg.display.set_caption("3d projection")
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    center = np.mat(dtype=np.double, data=[width / 2, height / 2]).T
    scale = 3

    points = [np.mat(dtype=np.double, data=[1, 1, 1]).T,
              np.mat(dtype=np.double, data=[2, 1, 1]).T]

    should_render = True

    while True:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    return

        if should_render:
            screen.fill(black)
            projected_points = []

            for point in points:
                projected = cam.project_point(point)
                projected = projected * scale + center
                projected_points.append(projected)
                pg.draw.circle(
                    screen, yellow, (projected[0, 0], projected[1, 0], 3))

            pg.draw.line(screen, white, (projected_points[0][0, 0], projected_points[0][1, 0]), (
                projected_points[1][0, 0], projected_points[1][1, 0]))
            pg.display.update()

            # should_render = False

            # l = [90, 45, 90]
            # for i in range(3):
            #     cam.angle[i, 0] = l[i]

            # q = cam._euler_to_quaternion()
            # cam.q = q
            # cam.q_con = cam._quaternion_conjugate()
            # print(q)

    # v = np.mat(dtype=np.double, data=[1, 0, 0, 1]).T
    # print(v)

    # print(cam.project_point(v))

    # cam.point[0, 0] = 3
    # cam.point[1, 0] = 5
    # cam.point[2, 0] = 15
    # v2 = cam.rotate_point(v)
    # print(cam.point)
    # cam.translate_x_pos()
    # print(np.round(v2, decimals=2))

    # print(cam.point)

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
