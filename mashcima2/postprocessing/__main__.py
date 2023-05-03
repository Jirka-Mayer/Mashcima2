from .foo import foo
from .quilt import quilt
from .seep import seep, layer_images, prepare_back_side
#import time
from PIL import Image
from skimage import util

# Lanuch me via:
# python3 -m mashcima2.postprocessing

print("Hello world, this is postprocessing!")
#print("Foo is:", foo())



seep(
    layer_images("mashcima2/postprocessing/generated_background.png", 
                 prepare_back_side("mashcima2/postprocessing/noty.png")),
    "mashcima2/postprocessing/noty.png")





#start = time.time()

image_path = ".\\mashcima2\\postprocessing\\default1.jpg"

foreground = Image.open(image_path)
foreground = util.img_as_float(foreground)

h, w, _ = foreground.shape

block_size = (min(h, w) - 1) // 2
num_block = 6
#mode = "Random"
#mode = "Best"
mode = "Cut"

#quilt(image_path, block_size, (num_block, num_block), mode).show()

#end = time.time()

#print(end - start)