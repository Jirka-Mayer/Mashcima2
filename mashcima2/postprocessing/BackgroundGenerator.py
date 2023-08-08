import numpy as np
import random
import os
import heapq
from skimage import util
from PIL import Image

from data.backgrounds.download_images import download


class BackgroundGenerator:
    def __init__(
        self,
        images_csv_path: str,
        rand = None,
        part_of_image_for_block_size: float = 1/3): #TODO: part_of_image_for_block_size should be in generate function or here?
        """
        Creates a new background generator with optional parameters.
        """
        self.images_csv_path = images_csv_path
        self.rand = random.Random() if rand is None else rand
        self.part_of_image_for_block_size = part_of_image_for_block_size
        self.images = download(images_csv_path) 
    
    def randomPatch(
        self,
        texture: np.ndarray, 
        block_size: int
    ) -> np.ndarray:
        h, w, _ = texture.shape
        i = np.random.randint(h - block_size)
        j = np.random.randint(w - block_size)

        return texture[i:i+block_size, j:j+block_size]
    
    def minCutPath(
        self,
        errors: np.ndarray):
        """
        Dijkstra's algorithm for finding the shortest path in a graph vertically.
        """
        pq = [(error, [i]) for i, error in enumerate(errors[0])]
        heapq.heapify(pq)

        h, w = errors.shape
        seen = set()

        while pq:
            error, path = heapq.heappop(pq)
            curDepth = len(path)
            curIndex = path[-1]

            if curDepth == h:
                return path

            for delta in -1, 0, 1:
                nextIndex = curIndex + delta

                if 0 <= nextIndex < w:
                    if (curDepth, nextIndex) not in seen:
                        cumError = error + errors[curDepth, nextIndex]
                        heapq.heappush(pq, (cumError, path + [nextIndex]))
                        seen.add((curDepth, nextIndex))
    
    def minCutPatch(
        self,
        patch: np.ndarray, 
        block_size: int, 
        overlap: int, 
        res: np.ndarray, 
        y: int, 
        x: int
    ) -> np.ndarray:
        patch = patch.copy()
        dy, dx, _ = patch.shape
        minCut = np.zeros_like(patch, dtype=bool)

        if x > 0:
            left = patch[:, :overlap] - res[y:y+dy, x:x+overlap]
            leftL2 = np.sum(left**2, axis=2)
            for i, j in enumerate(self.minCutPath(leftL2)):
                minCut[i, :j] = True

        if y > 0:
            up = patch[:overlap, :] - res[y:y+overlap, x:x+dx]
            upL2 = np.sum(up**2, axis=2)
            for j, i in enumerate(self.minCutPath(upL2.T)):
                minCut[:i, j] = True

        np.copyto(patch, res[y:y+dy, x:x+dx], where=minCut)

        return patch

    def generate(
        self,
        width_px: int,
        height_px: int,
        dpi: float # typical value 150
    ) -> np.ndarray:
        """
        Generates a background image.
        """
        #texture = random.choice([x for x in os.listdir("data/backgrounds/images/") if not x.startswith(".")])
        texture = random.choice(self.images)
        #texture = Image.open("data/backgrounds/images/" + texture) #TODO: do somehow differently without PIL maybe?
        texture = Image.open(texture) #TODO: do somehow differently without PIL maybe?
        texture = util.img_as_float(texture) #TODO: do somehow differently without skimage maybe?

        h, w, _ = texture.shape
        block_size = int((min(h, w) - 1) * self.part_of_image_for_block_size)

        num_blockHigh = height_px // block_size + 2
        num_blockWide = width_px // block_size + 2
        overlap = block_size // max(num_blockHigh, num_blockWide)

        h = (num_blockHigh * block_size) - (num_blockHigh - 1) * overlap
        w = (num_blockWide * block_size) - (num_blockWide - 1) * overlap

        result = np.zeros((h, w, texture.shape[2]))

        for i in range(num_blockHigh):
            for j in range(num_blockWide):
                y = i * (block_size - overlap)
                x = j * (block_size - overlap)

                # Fast sample and clean cut.
                patch = self.randomPatch(texture, block_size)
                patch = self.minCutPatch(patch, block_size, overlap, result, y, x)
                
                result[y:y+block_size, x:x+block_size] = patch
        
        result = (result * 255).astype(np.uint8)
        result = result[:height_px, :width_px]
        return result
    