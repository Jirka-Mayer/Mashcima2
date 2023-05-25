import cv2 as cv2
import numpy as np
import math

def bend_image(
    image: np.ndarray,
) -> np.ndarray:
    """ """

    map_x = np.zeros((image.shape[0], image.shape[1]), dtype=np.float32)
    map_y = np.zeros((image.shape[0], image.shape[1]), dtype=np.float32)

    # Bending the image.
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            map_x[y, x] = x
            #map_y[y, x] = y + (x - image.shape[1] / 2) ** 2 / 100
            #map_y[y, x] = math.sin(x) + y
            map_y[y, x] = math.sin(x / 100) * 50 + y

            if x > image.shape[1] / 5:
                map_y[y, x]  = y - x/4 + image.shape[1]/10 - 2

    image = cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR)

    return image