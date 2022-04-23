from camera import Camera
import numpy as np


def main():
    cam = Camera()

    l = [90, 45, 90]
    for i in range(3):
        cam.angle[i, 0] = l[i]

    q = cam._euler_to_quaternion()
    print(q)

    print(cam.angle)


main()
