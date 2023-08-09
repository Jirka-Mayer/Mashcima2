from .foo import foo
from .quilt import quilt
from .seep import seep_image, layer_images, prepare_back_side
from .geom_deformations import bend_image, bevel_image, change_perspective
from .handwriting_augmentation import augment
from .noise import kanungo
#import time
import cv2

# Lanuch me via:
# python3 -m mashcima2.postprocessing

print("Hello world, this is postprocessing!")
#print("Foo is:", foo())



# Launching the background generator via the class (correct API):
from mashcima2.postprocessing.BackgroundGenerator import BackgroundGenerator
generator = BackgroundGenerator("data/backgrounds/samples.csv", )
img = generator.generate(1024, 1024, 30)
print(img)
# cv2.imshow("", img)   
# cv2.waitKey(0)



# Launching the noise operations:
# image = cv2.imread("mashcima2/postprocessing/noty.png")
# image = kanungo(image)
# cv2.imshow("", image)
# cv2.waitKey(0)



# Launching the augmentation of handwritting:
#image = cv2.imread("mashcima2/postprocessing/noty.png")
#image = augment(image, -1)
#cv2.imshow("", image)
#cv2.waitKey(0)




# Launching the bending, beveling and changing perspective:
#image = cv2.imread("mashcima2/postprocessing/noty.png")
#image = bend_image(image)
#image = bevel_image(image)
#image = change_perspective(image)
#cv2.imshow("", image)
#cv2.waitKey(0)




# Launching the seep:
# back_side = cv2.imread("mashcima2/postprocessing/noty.png")
# backgroung_from_quilt = cv2.imread("mashcima2/postprocessing/generated_background.png")
# front_side = cv2.imread("mashcima2/postprocessing/noty.png")

# seeped_image = seep_image(back_side, backgroung_from_quilt, front_side)

# cv2.imshow("Seeped", seeped_image)
# cv2.waitKey(0)




# Launching the quilt:
#start = time.time()

# image_path = ".\\mashcima2\\postprocessing\\default1.jpg"

# foreground = Image.open(image_path)
# foreground = util.img_as_float(foreground)

# h, w, _ = foreground.shape

# block_size = (min(h, w) - 1) // 2
# num_block = 6
# #mode = "Random"
# #mode = "Best"
# #mode = "Cut"
# mode = "RandomCut"

# quilt(image_path, block_size, (num_block, num_block), mode).show()

#end = time.time()
#print(end - start)