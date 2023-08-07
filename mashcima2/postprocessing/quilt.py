from .patch import randomPatch, randomBestPatch, minCutPatch

import numpy as np
from PIL import Image
from skimage import util

def quilt(
        image_path: str, 
        block_size: int, 
        num_block: int, 
        mode: str, 
        sequence: bool=False
) -> Image:
    texture = Image.open(image_path)
    texture = util.img_as_float(texture)

    overlap = block_size // max(num_block)
    num_blockHigh, num_blockWide = num_block

    h = (num_blockHigh * block_size) - (num_blockHigh - 1) * overlap
    w = (num_blockWide * block_size) - (num_blockWide - 1) * overlap

    res = np.zeros((h, w, texture.shape[2]))

    for i in range(num_blockHigh):
        for j in range(num_blockWide):
            y = i * (block_size - overlap)
            x = j * (block_size - overlap)

            if i == 0 and j == 0 or mode == "Random":
                patch = randomPatch(texture, block_size)
            elif mode == "Best":
                patch = randomBestPatch(texture, block_size, overlap, res, y, x)
            elif mode == "Cut":
                patch = randomBestPatch(texture, block_size, overlap, res, y, x)
                patch = minCutPatch(patch, block_size, overlap, res, y, x)
            
            # Kompromis: rychlý sample a čistý střih
            # Na šumové textury pozadí to stačí. Jirka.
            elif mode == "RandomCut":
                patch = randomPatch(texture, block_size)
                patch = minCutPatch(patch, block_size, overlap, res, y, x)
            
            res[y:y+block_size, x:x+block_size] = patch
    
    image = Image.fromarray((res * 255).astype(np.uint8))
    return image
