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
    pg.init()
    pg.display.set_caption("3d projection")
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    center = np.mat(dtype=np.double, data=[width / 2, height / 2]).T
    scale = 300

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

    first_time = True

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
                elif event.key == pg.K_z:
                    cam.zoom_in()
                elif event.key == pg.K_x:
                    cam.zoom_out()
                elif event.key == pg.K_v:
                    cam.rotate_x_pos()
                elif event.key == pg.K_b:
                    cam.rotate_x_neg()
                elif event.key == pg.K_n:
                    cam.rotate_y_pos()
                elif event.key == pg.K_m:
                    cam.rotate_y_neg()
        keys = pg.key.get_pressed()

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
        else:
            if len(pg.event.get()) == 0 and not first_time:
                first_time = False
                continue

        screen.fill(black)

        for i, cuboid in enumerate(cuboids):
            lines = cuboid.to_list_of_lines(cam, scale, center)
            for line in lines:
                pg.draw.line(screen, colors[i], line[0], line[1])

        pg.display.update()


main()
