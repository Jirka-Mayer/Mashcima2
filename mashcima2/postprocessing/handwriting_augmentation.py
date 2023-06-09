import cv2 as cv2
import numpy as np
from scipy import ndimage

def augment(
    image: np.ndarray,
    direction: int, # 1 or -1, defines slant of the handwriting
    # size_of_kernel: int, # depends on pixels per staff space, TODO: implement
) -> np.ndarray:
    """ Augments the image by dilating and eroding it to look like handwritten. """
    
    dil_kernel = np.asarray([[0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0]],
                      dtype=np.uint8)
    
    ero_kernel = np.asarray([[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]],
                      dtype=np.uint8)
    

    # Inverting the image to work with white notes on black background.
    image = cv2.bitwise_not(image)

    # Rotating the kernel to match the direction of the handwriting.
    dil_kernel = ndimage.rotate(dil_kernel, direction * 45, reshape=True) 
    image = cv2.dilate(image, dil_kernel, iterations=1)

    #TODO: rotate using not scipy

    ero_kernel = ndimage.rotate(ero_kernel, direction * 45, reshape=True)
    image = cv2.erode(image, ero_kernel, iterations=1, anchor = (-1,-1))

    image = cv2.bitwise_not(image)

    return image