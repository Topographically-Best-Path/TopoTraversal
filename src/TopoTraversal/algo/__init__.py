import TopoTraversal.constants as constants
import TopoTraversal.gui as gui
import TopoTraversal.data as data

from typing import Tuple
from typing import List
import heapq
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
    start_ind = (-1, -1)
    end_ind = (-1, -1)
    for lat_ind, row in enumerate(dat):
        for long_ind, entry in enumerate(row):
            # Check that the coordinates match
            if math.isclose(entry[1], start[0], abs_tol=0.001) and math.isclose(entry[0], start[1], abs_tol=0.001):
                start_ind = (lat_ind, long_ind)
            if math.isclose(entry[1], end[0], abs_tol=0.001) and math.isclose(entry[0], end[1], abs_tol=0.001):
                end_ind = (lat_ind, long_ind)
    if start_ind == (-1, -1):
        print("UH OH")

    # Set up the distance and previous traversal matrices for Djikstra
    dists : List[List[int]] = [[math.inf for _ in dat[0]] for __ in dat]
    prev : List[List[Tuple[int, int]]] = [[(-1, -1) for _ in dat[0]] for __ in dat]
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
                if (dat[nextx][nexty][2] - dat[coord[0]][coord[1]][2]) / scale <= threshold: # slope check
                    if curr_dist + 1 < dists[nextx][nexty]: # dists check
                        dists[nextx][nexty] = curr_dist + 1
                        prev[nextx][nexty] = coord
                        heapq.heappush(q, (curr_dist + 1, (nextx, nexty)))

    # Reconstruct the path if the end has been reached
    if prev[end_ind[0]][end_ind[1]] != (-1, -1):
        ans:List[Tuple[float, float]] = []

        # Starting from the end, add the float coordinates
        curr = end_ind
        while curr != (-1, -1):
            ans.append(dat[curr[0]][curr[1]][:2])
            curr = prev[curr[0]][curr[1]]
        ans.reverse()
        # Check that the beginning float coordinates are correct
        if math.isclose(ans[0][1], start[0], abs_tol=0.001) and math.isclose(ans[0][0], start[1], abs_tol=0.001):
            print("Success")
        return ans

    return []
