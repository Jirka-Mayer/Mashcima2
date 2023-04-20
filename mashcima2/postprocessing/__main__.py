from .foo import foo
from .quilt import quilt
#import time
from PIL import Image
from skimage import util

# Lanuch me via:
# python3 -m mashcima2.postprocessing

print("Hello world, this is postprocessing!")
#print("Foo is:", foo())

#start = time.time()

image_path = ".\\mashcima2\\postprocessing\\default1.jpg"

image = Image.open(image_path)
image = util.img_as_float(image)

h, w, _ = image.shape

block_size = (min(h, w) - 1) // 2
num_block = 6
#mode = "Random"
#mode = "Best"
mode = "Cut"

quilt(image_path, block_size, (num_block, num_block), mode).show()

#end = time.time()

#print(end - start)