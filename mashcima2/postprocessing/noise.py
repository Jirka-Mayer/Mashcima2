import cv2 as cv2
import numpy as np
import random

def kanungo(
    image: np.ndarray,
    alpha: float = 0.3,  # 
    alpha0: float = 0.5,  #
) -> np.ndarray:
    """ ocekava cerne symboly na bilem pozadi """

    # Converting the image to greyscale.
    greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Creating a binary image.
    T, thresh = cv2.threshold(greyscale, 127, 255, cv2.THRESH_BINARY)
    
    # Computing the distance transform for the both foreground and background.
    dist_map_background = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    dist_map_foreground = cv2.distanceTransform(1 - thresh, cv2.DIST_L2, 5)

    # Computing the probability of flipping the pixel.
    r = np.random.rand(dist_map_background.shape[0], dist_map_background.shape[1])
    probability_background = alpha0 * np.exp(-alpha * dist_map_background * dist_map_background)
    probability_background[thresh == 0] = 0

    r = np.random.rand(dist_map_foreground.shape[0], dist_map_foreground.shape[1])
    probabilty_foreground = alpha0 * np.exp(-alpha * dist_map_foreground * dist_map_foreground)
    probabilty_foreground[thresh == 255] = 0

    # Generating the noise by flipping the pixels according to the probability.
    probabilty = probability_background + probabilty_foreground
    mask = r < probabilty   # na polickach matice je bud True nebo False 
    thresh[mask] = 1 - thresh[mask]
    
    return thresh
