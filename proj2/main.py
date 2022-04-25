from typing import List
from camera import Camera
import numpy as np
import pygame as pg
from cuboid import Cuboid


def main():
    width, height = 1000, 800
    black = (30, 30, 30)
    white = (255, 255, 255)
    yellow = (249, 215, 28)
    green = (0, 128, 0)
    colors = [white, yellow, green]

    cam = Camera()
    # pg.init()
    # pg.display.set_caption("3d projection")
    # screen = pg.display.set_mode((width, height))
    # clock = pg.time.Clock()
    # center = np.mat(dtype=np.double, data=[width / 2, height / 2]).T
    # scale = 300

    # points = [np.mat(dtype=np.double, data=[1, 1, 1]).T,
    #           np.mat(dtype=np.double, data=[2, 1, 1]).T]

    cuboids: List[Cuboid] = []
    cube_1 = Cuboid([np.mat(dtype=np.double, data=[-1, -1, 1]).T,
                     np.mat(dtype=np.double, data=[1, -1, 1]).T,
                     np.mat(dtype=np.double, data=[1, 1, 1]).T,
                     np.mat(dtype=np.double, data=[-1, 1, 1]).T,
                     np.mat(dtype=np.double, data=[-1, -1, -1]).T,
                     np.mat(dtype=np.double, data=[1, -1, -1]).T,
                     np.mat(dtype=np.double, data=[1, 1, -1]).T,
                     np.mat(dtype=np.double, data=[-1, 1, -1]).T])
    cube_2 = Cuboid([np.mat(dtype=np.double, data=[-1, -1, 1-5]).T,
                     np.mat(dtype=np.double, data=[1, -1, 1-5]).T,
                     np.mat(dtype=np.double, data=[1, 1, 1-5]).T,
                     np.mat(dtype=np.double, data=[-1, 1, 1-5]).T,
                     np.mat(dtype=np.double, data=[-1, -1, -1-5]).T,
                     np.mat(dtype=np.double, data=[1, -1, -1-5]).T,
                     np.mat(dtype=np.double, data=[1, 1, -1-5]).T,
                     np.mat(dtype=np.double, data=[-1, 1, -1-5]).T])
    cuboids.append(cube_1)
    cuboids.append(cube_2)

    # should_render = True
    # first_time = True

    # cam.angle = np.mat(data=[90, 45, 90]).T
    print(np.round(cam.get_transform(), decimals=2))
    p = cam.project_point(np.mat(dtype=np.double, data=[-1, -1, 1, 1]).T)
    print(np.round(p, decimals=2))

    while False:
        clock.tick(60)
        # should_render = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    return
                elif event.key == pg.K_z:
                    cam.zoom_in()
                elif event.key == pg.K_x:
                    cam.zoom_out()
                # elif event.key == pg.K_a:
                #     cam.translate_x_neg()
                # elif event.key == pg.K_d:
                #     cam.translate_x_pos()
                # should_render = True
        keys = pg.key.get_pressed()

        # suma = 0
        # for key in keys:
        #     suma += key
        # print(suma)

        if keys[pg.K_d] > 0:
            cam.translate_x_neg()
        elif keys[pg.K_a] > 0:
            cam.translate_x_pos()
        elif keys[pg.K_w] > 0:
            cam.translate_y_pos()
        elif keys[pg.K_s] > 0:
            cam.translate_y_neg()
        elif keys[pg.K_q] > 0:
            cam.translate_z_pos()
        elif keys[pg.K_e] > 0:
            cam.translate_z_neg()
        elif keys[pg.K_k] > 0:
            cam.rotate_x_neg()
        elif keys[pg.K_i] > 0:
            cam.rotate_x_pos()
        elif keys[pg.K_l] > 0:
            cam.rotate_y_pos()
        elif keys[pg.K_j] > 0:
            cam.rotate_y_neg()
        elif keys[pg.K_u] > 0:
            cam.rotate_z_pos()
        elif keys[pg.K_o] > 0:
            cam.rotate_z_neg()
        # else:
        #     should_render = False

        # if should_render or first_time:
            # first_time = False
        screen.fill(black)

        for i, cuboid in enumerate(cuboids):
            lines = cuboid.to_list_of_lines(cam, scale, center)
            for line in lines:
                # print(line)
                pg.draw.line(screen, colors[i], line[0], line[1])

            # should_render = False
        pg.display.update()

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
