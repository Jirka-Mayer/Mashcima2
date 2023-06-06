import mung
import mung.io
from mung.node import Node
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import cv2

DPSS = 28.5
RADIUS_SP = 6

# inpupt data
img_path = "/home/jirka/Datasets/CVCMUSCIMA_WI/PNG_GT_BW/w-03/p001.png"
image = cv2.imread(img_path, cv2.IMREAD_COLOR)
nodes: List[Node] = mung.io.read_nodes_from_file(
    "/home/jirka/Datasets/MuscimaPlusPlus/v2.0/data/annotations/" +
    "CVC-MUSCIMA_W-03_N-01_D-ideal.xml"
)

# img = np.ones(shape=image.shape, dtype=np.float)

# noteheads: List[Node] = [n for n in nodes if "notehead" in n.class_name]
# left_deltas = []
# top_deltas = []

# for notehead in noteheads:
#     # print(notehead)
#     notehead.render(img, alpha=0.7)

#     # neighborhood
#     for n in noteheads:
#         if n is notehead: continue
#         distance_sp = (n.right - notehead.left) / DPSS
#         if distance_sp > 0: continue
#         if abs(distance_sp) > RADIUS_SP: continue
#         left_deltas.append(distance_sp)
#         top_deltas.append((n.top - notehead.bottom) / DPSS)

# plt.imshow(img)
# plt.show()

# print(list(sorted(left_deltas)))
# plt.hist(left_deltas, bins=30)
# plt.show()

# plt.plot(left_deltas, top_deltas, "x")
# plt.show()

# plt.hist2d(left_deltas, top_deltas, bins=20)
# plt.show()

def print_node(img, node: Node):
    m = np.dstack([node.mask, node.mask, node.mask])
    img[node.top:node.bottom, node.left:node.right] *= 1.0 - m

"""
THE IDEA
--------

The score is drawn by someone as sequence of pen strokes. This can be clustered
as a sequence of symbol-drawing actions. Therefore we can take the music notation
primitives and order them temporarily as they are drawn. This sequence is the input
sequence. The predicted output is the position (and style?) of the next (current)
symbol to be drawn.

Ultimately this can be done the same way as Alex Graves handwriting synthesis.
But for now, let's do simple empirical distribution modelling.

Example input sequence and output values
    clef-f          move from the staff start to the clef center
    keySignature    do-nothing (or update internal state)
    sharp-fis       move to sharp center, draw sharp
    time-signature  ...
    5
    4
    ledger line (up 1)
    notehead (quarter, high)
    stem (down)
    natural

When drawing the current symbol, you know:
- what was the last drawn symbol AND where it was placed
- what symbol is being drawn
- after you sample the symbol mask, you know its properties
- you know the staff properties, remaining space, and other context
"""

# noteheads: List[Node] = [n for n in nodes if "notehead" in n.class_name]

img = np.ones(shape=image.shape, dtype=np.float)
for n in nodes:
    if n.class_name == "staffLine":
        print_node(img, n)

interestingClasses = set([
    "noteheadFull", "noteheadHalf",
    "ledgerLine",
    "restQuarter", "rest8th", "rest16th",
    "stem",
    "beam",
    "barline",
    "staffLine"
])

staves = {n.id: n for n in nodes if n.class_name == "staff"}

nodes_by_staff = [
    [n for n in nodes if (staff_id in n.outlinks) and ("notehead" in n.class_name)]
    for staff_id, staff in staves.items()
]

for i in range(len(nodes_by_staff)):
    items = nodes_by_staff[i]
    nodes_by_staff[i] = list(sorted(items, key=lambda x: x.left))

deltas_left = []
deltas_top = []
for i in range(len(nodes_by_staff)):
    p = 0
    last = None
    for n in nodes_by_staff[i]:
        print_node(img, n)
        if n.left < p + DPSS * 6:
            n.render(img, alpha=0.7)
        
            if last is not None:
                deltas_left.append((n.left - last.left) / DPSS)
                deltas_top.append((n.top - last.top) / DPSS)

        p = n.left
        last = n


# plt.hist2d(deltas_left, deltas_top, bins=10)
# plt.plot(deltas_left, deltas_top, "x")
plt.hist(deltas_left, bins=10)
# plt.hist(deltas_top, bins=10)
plt.show()

plt.imshow(img)
plt.show()
