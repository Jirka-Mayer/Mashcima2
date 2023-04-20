import numpy as np
import heapq
# import matplotlib.pyplot as plt


def randomPatch(
        texture: np.ndarray, 
        block_size: int
) -> np.ndarray:
    """Function for mode: Random."""
    h, w, _ = texture.shape
    i = np.random.randint(h - block_size)
    j = np.random.randint(w - block_size)

    return texture[i:i+block_size, j:j+block_size]


def L2OverlapDiff(
        patch: np.ndarray, 
        block_size: int, 
        overlap: int, 
        res: np.ndarray, 
        y: int, 
        x: int
) -> float:
    """Help function for mode: Best."""
    error = 0
    if x > 0:
        left = patch[:, :overlap] - res[y:y+block_size, x:x+overlap]
        error += np.sum(left**2)

    if y > 0:
        up   = patch[:overlap, :] - res[y:y+overlap, x:x+block_size]
        error += np.sum(up**2)

    if x > 0 and y > 0:
        corner = patch[:overlap, :overlap] - res[y:y+overlap, x:x+overlap]
        error -= np.sum(corner**2)

    return error

def randomBestPatch(
        texture: np.ndarray, 
        block_size: int, 
        overlap: int, 
        res: np.ndarray, 
        y: int, 
        x: int
) -> np.ndarray:
    """Function for mode: Best."""
    h, w, _ = texture.shape
    errors = np.zeros((h - block_size, w - block_size))

    for i in range(h - block_size):
        for j in range(w - block_size):
            patch = texture[i:i+block_size, j:j+block_size]
            e = L2OverlapDiff(patch, block_size, overlap, res, y, x)
            errors[i, j] = e
    
    # plt.imshow(errors)
    # plt.show()

    i, j = np.unravel_index(np.argmin(errors), errors.shape)
    return texture[i:i+block_size, j:j+block_size]


def minCutPath(errors: np.ndarray):
    """Help function for mode: Cut."""
    # dijkstra's algorithm vertical
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
        patch: np.ndarray, 
        block_size: int, 
        overlap: int, 
        res: np.ndarray, 
        y: int, 
        x: int
) -> np.ndarray:
    """Function for mode: Cut."""
    patch = patch.copy()
    dy, dx, _ = patch.shape
    minCut = np.zeros_like(patch, dtype=bool)

    if x > 0:
        left = patch[:, :overlap] - res[y:y+dy, x:x+overlap]
        leftL2 = np.sum(left**2, axis=2)
        for i, j in enumerate(minCutPath(leftL2)):
            minCut[i, :j] = True

    if y > 0:
        up = patch[:overlap, :] - res[y:y+overlap, x:x+dx]
        upL2 = np.sum(up**2, axis=2)
        for j, i in enumerate(minCutPath(upL2.T)):
            minCut[:i, j] = True

    np.copyto(patch, res[y:y+dy, x:x+dx], where=minCut)

    return patch
