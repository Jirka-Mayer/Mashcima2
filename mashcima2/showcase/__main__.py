import matplotlib.pyplot as plt
import cv2
import numpy as np

from ..postprocessing.handwriting_augmentation import augment
from ..postprocessing.quilt import quilt
from ..postprocessing.seep import prepare_back_side

# Lanuch me via:
# python3 -m mashcima2.showcase

def resize(img, scale):
    return cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)))

def alpha_blend(foreground, background, alpha):
    alpha = np.dstack([alpha] * 3)
    return (foreground * alpha + background * (1 - alpha)).astype(np.uint8)

# load images
MUSCIMA = "/home/jirka/Datasets/CVCMUSCIMA_WI"
PAGE = "w-01/p003.png"
withStaff = cv2.imread(MUSCIMA + "/PNG_GT_BW/" + PAGE)
noStaff = cv2.imread(MUSCIMA + "/PNG_GT_NoStaff/" + PAGE)

stafflines = withStaff - noStaff
foreground = noStaff

# resize and invert
stafflines = resize(255 - stafflines, scale=0.5)
foreground = resize(255 - foreground, scale=0.5)

# augment foreground
foreground = augment(foreground, 0.1)

# create notation layer (stafflines + notes)
notation = alpha_blend(foreground, stafflines, (255 - foreground[:,:,0]) / 255)

# create seep layer
seep = prepare_back_side(notation)
seep = seep[0:notation.shape[0], 0:notation.shape[1], :]

# create paper background
BLOCK_SIZE=64
background = quilt(
    image_path="mashcima2/postprocessing/default1.jpg",
    block_size=BLOCK_SIZE,
    num_block=(
        int(foreground.shape[0] * (7/6) / BLOCK_SIZE) + 2,
        int(foreground.shape[1] * (7/6) / BLOCK_SIZE) + 2
    ),
    mode="RandomCut"
)
background = np.array(background)
background = background[0:foreground.shape[0], 0:foreground.shape[1], :]

# compose
img = alpha_blend(seep, background, (255 - seep[:,:,0]) / 255 * 0.3)
img = alpha_blend(notation, img, (255 - notation[:,:,0]) / 255 * 0.8)

plt.imshow(img)
plt.show()
# cv2.imwrite("/home/jirka/Downloads/synthetic.png", np.dstack([
#     img[:,:,2], img[:,:,1], img[:,:,0] # rgb to bgr
# ]))
