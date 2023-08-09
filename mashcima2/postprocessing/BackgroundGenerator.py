import numpy as np
import random
import heapq
import cv2

from data.backgrounds.download_images import download

class BackgroundGenerator:
    def __init__(
        self,
        images_csv_path: str,
        rand = None,
        part_of_image_for_block_size: float = 1/3,
        overlap_ratio: float = 0.1):
        """
        Creates a new background generator with optional parameters.
        """
        self.images_csv_path = images_csv_path
        self.rand = random.Random() if rand is None else rand
        self.part_of_image_for_block_size = part_of_image_for_block_size
        self.overlap_ratio = overlap_ratio
        self.images = download(images_csv_path) 
    
    def randomPatch(
        self,
        texture: np.ndarray, 
        block_size: int
    ) -> np.ndarray:
        """
        Returns a random patch of the given texture.
        """
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
        # Sorting just dpi-valid textures.
        valid_textures = [x for x in self.images if int(x.split("_")[-1][:-4]) >= dpi] 

        # If no textures with dpi >= dpi are found, raising an exception.
        if len(valid_textures) == 0:
            raise Exception(f"No textures in file {self.images_csv_path} with dpi >= {dpi} found.")
        
        # Choosing a random texture from the valid ones.
        texture_path = self.rand.choice(valid_textures)
        #texture_path = "./data/backgrounds/images/6cfd34b3-cfdf-41b7-9c37-0b8466ab8880_176_132_397_459_150.jpg"
        texture_dpi = int(texture_path.split("_")[-1][:-4])

        texture = cv2.imread(texture_path).astype(np.float32) / 255.0
        scale_factor = dpi / texture_dpi
        dsize = (int(texture.shape[1] * scale_factor), int(texture.shape[0] * scale_factor))
        texture = cv2.resize(texture, dsize, interpolation=cv2.INTER_AREA)

        h, w, _ = texture.shape
        block_size = int((min(h, w) - 1) * self.part_of_image_for_block_size)

        overlap = int(block_size * self.overlap_ratio)
        if overlap == 0:
            raise Exception("Overlap is 0px.")
        num_blockHigh = height_px // (block_size - overlap) + 2
        num_blockWide = width_px // (block_size - overlap) + 2

        h = (num_blockHigh * block_size) - (num_blockHigh - 1) * overlap
        w = (num_blockWide * block_size) - (num_blockWide - 1) * overlap

        result = np.zeros((h, w, texture.shape[2]))

        for i in range(num_blockHigh):
            for j in range(num_blockWide):
                y = i * (block_size - overlap)
                x = j * (block_size - overlap)

                # Fast sample and clean cut.
                patch = self.randomPatch(texture, block_size)
                patch = self.minCutPatch(patch, overlap, result, y, x)
                
                result[y:y+block_size, x:x+block_size] = patch
        
        result = (result * 255).astype(np.uint8)
        over_height = result.shape[0] - height_px
        over_width = result.shape[1] - width_px
        offset_height = self.rand.randint(0, over_height)
        offset_width = self.rand.randint(0, over_width)
        result = result[offset_height:height_px + offset_height, offset_width:width_px + offset_width]
        return result
    