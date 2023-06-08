import cv2 as cv2
import numpy as np

def augment(
    image: np.ndarray,
    # direction: np.ndarray,
) -> np.ndarray:
    """  """


    direction0 = np.ones((3, 3), np.uint8)
    
    direction1 = np.asarray([[1, 0, 0, 0, 0], 
                            [0, 1, 0, 0, 0],
                            [0, 0, 1, 0, 0], 
                            [0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 1]],
                            dtype=np.uint8)
    direction2 = np.asarray([[1, 1, 1, 1, 0], 
                            [1, 1, 1, 0, 1],
                            [1, 1, 0, 1, 1], 
                            [1, 0, 1, 1, 1],
                            [0, 1, 1, 1, 1]],
                            dtype=np.uint8)
    direction3 = np.asarray([[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]],
                            dtype=np.uint8)
    direction4 = np.asarray([[1, 1],
                            [1, 1]],
                            dtype=np.uint8)
    direction5 = np.asarray([[1, 0, 0, 0, 1],
                     [1, 0, 0, 0, 1],
                     [1, 0, 0, 0, 1],
                     [1, 0, 0, 0, 1],
                     [1, 0, 0, 0, 1]],
                     dtype=np.uint8)
    

    dil = np.asarray([[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1]],
                      dtype=np.uint8)
    
    ero = np.asarray([[0, 0, 0, 0, 1],
                      [0, 0, 0, 1, 0],
                      [0, 0, 1, 0, 0],
                      [0, 1, 0, 0, 0],
                      [1, 0, 0, 0, 0]],
                      dtype=np.uint8)
    


    image = cv2.bitwise_not(image)

    image = cv2.dilate(image, dil, iterations=1)
    image = cv2.erode(image, ero, iterations=1, anchor = (2,2))

    image = cv2.bitwise_not(image)

    return image