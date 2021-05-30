from typing import Tuple
from typing import List
import numpy as np
import constants
import heapq
import data
import math

def read() -> List[List[Tuple[float, float, float]]]:
    """
    Reads points from the file written by the data module into a 2D list.
    The way the data is structured from the query, longitude varies before latitude, and comes first in the pair.
    Therefore, in returned read, latitude is measured by row index and longitude is measured by column index.
    Returns:
    tuple(float, list(list(float, float, float))):
    - the single float is the distance scale between points
    - the 2D list is the heights and places
    """
    points_result = []
    current_lat = None
    with open(constants.TEMPDIR / "Data.csv") as fin:
        # Read the data
        datgen = [[*map(float, line.split(','))] for line in fin.readlines()]
        for dat in datgen:
            if len(dat) == 3:
                # Add a new row
                if current_lat is None or not math.isclose(dat[1], current_lat):
                    points_result.append([])
                    current_lat = dat[1]

                # The actual contents: [long, lat, heights]
                points_result[-1].append(dat)
    return points_result

def get_path(start:Tuple[float, float], end:Tuple[float, float], scale:float, threshold: float) -> List[Tuple[float, float]]:
    """
    The heart of our project: the algorithm.
    Parameters:
    Threshold -> float: returns threshold
    Returns:
    The list of float coordinates
    """

    dat:List[List[Tuple[float, float, float]]] = read()
    # Find the indices of the start and end
    npdat = np.array(dat)
    start_ind = np.unravel_index(
        np.argmin(
            (npdat[:,:,0] - start[0]) ** 2 + 
            (npdat[:,:,1] - start[1]) ** 2
        ), 
    npdat[:,:,0].shape)
    end_ind = np.unravel_index(
        np.argmin(
            (npdat[:,:,0] - end[0]) ** 2 + 
            (npdat[:,:,1] - end[1])** 2
        ), 
    npdat[:,:,0].shape)

    # Set up the distance and previous traversal matrices for Djikstra
    dists = np.full(npdat[:,:,0].shape, np.inf)
    prev = np.full(npdat[:,:,:2].shape, -1)
    dists[start_ind[0]][start_ind[1]] = 0

    # Start Djikstra
    q:list = []
    heapq.heappush(q, (0, start_ind))
    dxy = [(-1, 0), (0, 1), (1, 0), (0, -1)] # Constants for checking neighbors
    while len(q) > 0:
        # Pop the current minimum total distance from beginning
        try:
            curr_dist, coord = heapq.heappop(q)
        except:
            print(q)

        # Break upon encountering the end; if its in the heap, it must have its dists/prev updated
        if coord == end:
            break

        # Check all neighbors
        for delta in dxy:
            nextx = coord[0] + delta[0]
            nexty = coord[1] + delta[1]

            if 0 <= nextx < len(dat) and 0 <= nexty < len(dat[0]): # bounds check
                if (npdat[nextx][nexty][2] - npdat[coord[0]][coord[1]][2]) / scale <= threshold: # slope check
                    if curr_dist + 1 < dists[nextx][nexty]: # dists check
                        dists[nextx][nexty] = curr_dist + 1
                        prev[nextx][nexty][0] = coord[0]
                        prev[nextx][nexty][1] = coord[1]
                        heapq.heappush(q, (curr_dist + 1, (nextx, nexty)))

    # Reconstruct the path if the end has been reached
    if prev[end_ind[0]][end_ind[1]][0] != -1 and prev[end_ind[0]][end_ind[1]][1] != -1 :
        ans:List[Tuple[float, float]] = []

        # Starting from the end, add the float coordinates
        curr = end_ind
        while curr != (-1, -1):
            ans.append((npdat[curr[0]][curr[1]][0], npdat[curr[0]][curr[1]][1]))
            curr = (prev[curr[0]][curr[1]][0], prev[curr[0]][curr[1]][1])
        ans.reverse()
        return ans

    return []

def main():
    data.create_temp_dir()
    data.get_etopo_data(-74,40,3)
    data.create_image()
    pts = get_path((-71.0, 43.0), (-77.0, 43.0), data.get_scale()[0], 0.25)
    print(pts)
    data.plot_points(pts)

if __name__ == "__main__":
    main()
