from .foo import foo
from .quilt import quilt
#import time

# Lanuch me via:
# python3 -m mashcima2.postprocessing

print("Hello world, this is postprocessing!")
#print("Foo is:", foo())

#start = time.time()

image_path = ".\\mashcima2\\postprocessing\\apple.jpg"
block_size = 50
num_block = 6
#mode = "Random"
#mode = "Best"
mode = "Cut"

quilt(image_path, block_size, (num_block, num_block), mode).show()

#end = time.time()

#print(end - start)