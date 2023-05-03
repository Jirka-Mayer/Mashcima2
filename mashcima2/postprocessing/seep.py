from PIL import Image
import cv2 as cv2

def prepare_back_side(
        image_path: str,
        output_path: str = "mashcima2/postprocessing/prepared_back_side.png"
) -> str:
    """Blurs the image and rotates it along the y axis. Saves the result and returns path to it."""
    image = cv2.imread(image_path)

    # Bluring the image.
    image = cv2.blur(image, (10, 10))

    # Rotation along the y axis => parameter 1, along the x axis => parameter 0
    image = cv2.flip(image, 1)

    # Saving the image.
    cv2.imwrite(output_path, image)

    return output_path


def layer_images(
        background_path: str,
        foreground_path: str,
        alpha: float = 0.5,
        output_path: str = "mashcima2/postprocessing/layered_background.png"
) -> str:
    """Layers two images on top of each other."""
    background = cv2.imread(background_path)
    foreground = cv2.imread(foreground_path)

    # Cut the images to the same size.
    x_shape = min(background.shape[0], foreground.shape[0])
    y_shape = min(background.shape[1], foreground.shape[1])

    background = background[0:x_shape, 0:y_shape]
    foreground = foreground[0:x_shape, 0:y_shape]

    beta = ( 1.0 - alpha )
    result = cv2.addWeighted(background, alpha, foreground, beta, 0.0)

    cv2.imwrite(output_path, result)

    return output_path


def seep(
        seep_path: str,
        image_path: str,
):
    """TODO"""  

    result = layer_images(seep_path, image_path, output_path="mashcima2/postprocessing/seeped.png")

    cv2.imshow("Seeped", cv2.imread(result))

