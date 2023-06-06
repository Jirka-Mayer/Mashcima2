import mung
import mung.io
from mung.node import Node
from mung2midi.inference import OnsetsInferenceEngine
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import cv2

def print_node(img, node: Node):
    m = np.dstack([node.mask, node.mask, node.mask])
    img[node.top:node.bottom, node.left:node.right] *= 1.0 - m

# inpupt data
img_path = "/home/jirka/Datasets/CVCMUSCIMA_WI/PNG_GT_BW/w-03/p001.png"
image = cv2.imread(img_path, cv2.IMREAD_COLOR)
nodes: List[Node] = mung.io.read_nodes_from_file(
    "/home/jirka/Datasets/MuscimaPlusPlus/v2.0/data/annotations/" +
    "CVC-MUSCIMA_W-03_N-01_D-ideal.xml"
)

# # precedence graph
# engine = OnsetsInferenceEngine(nodes)
# # engine.measure_separators = None # fix strict python stuff
# # engine.measure_separators = [c for c in nodes if c.class_name == 'measureSeparator']
# g = engine.infer_precedence_from_annotations(nodes)
# print(g)
# exit()

# render output image
# img = np.zeros(shape=(1528, 3479, 3), dtype=np.float)
# img = 1.0 - image
img = np.ones(shape=image.shape, dtype=np.float)

for node in nodes:
    if "barline" in node.class_name:
        # print_node(img, node)
        node.render(img, alpha=0.7)
    if "notehead" in node.class_name:
        # print_node(img, node)
        node.render(img, alpha=0.7)
    if "rest" in node.class_name:
        # print_node(img, node)
        node.render(img, alpha=0.7)
    
    if node.class_name == "staffLine":
        print_node(img, node)

plt.imshow(img)
plt.show()
