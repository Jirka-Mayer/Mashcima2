import cv2 as cv2
import numpy as np
import math

def bend_image(
    image: np.ndarray,
) -> np.ndarray:
    """ Bends the image as it was from a book. """

    map_x = np.zeros((image.shape[0], image.shape[1]), dtype=np.float32)
    map_y = np.zeros((image.shape[0], image.shape[1]), dtype=np.float32)

    # The constant to add to the linear function.
    constant = 0             

    # 20% of the image will be bended.   
    part_of_image_to_bend = 1/5 

    # The gradient of the linear function.
    gradient = 1/6              

    # Bending the image.

    for row in range(image.shape[0]):
        for column in range(image.shape[1]):
            map_x[row, column] = column         

            # The "bended" part from the spine of the book. Using sine function.        
            map_y[row, column] = row + 50 * math.sin(column / 100)

            # Computing the constant to add to the linear function for "straight" part.
            if column > image.shape[1] * part_of_image_to_bend and constant == 0:
                constant = map_y[row, column] + map_x[row, column] * gradient

            # The "straight" part of the paper from the book. Using linear function.
            if column > image.shape[1] * part_of_image_to_bend:
                map_y[row, column]  = row - column * gradient + constant

    image = cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR)

    return image