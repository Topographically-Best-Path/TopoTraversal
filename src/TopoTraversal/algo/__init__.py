import typing
import TopoTraversal.constants as constants

def read() -> typing.Tuple[float, typing.List[typing.List[float]]]:
    """
    Reads points from the file written by the data module into a 2D list.

    The way the data is structured from the query, longitude varies before latitude. 
    Therefore, in returned read, longitude is measured by column index and latitude is measured by row index.
    Returns:
    tuple(float, list(list(float))): 
    - the single float is the distance scale between points
    - the 2D list is the heights
    """
    scale_result = None
    points_result = []
    current_lat = None
    with open(constants.TEMPDIR / "temp.txt") as fin:
        # Read the data
        datgen = ([*map(float, line.split())] for line in fin.readlines())
        for dat in datgen:
            # Add a new row 
            if dat[0] != current_lat:
                points_result.append([])
                
                # Find scale result from latitude difference
                if scale_result == None and current_lat != None:
                    scale_result = abs(dat[0] - current_lat)

                current_lat = dat[0]
            # The actual contents: heights
            points_result[-1].append(dat[2])

    return (scale_result, points_result)

def get_path(threshold: float):
    """
    The heart of our project: the algorithm.
    Parameters:
    Threshold -> float: returns threshold
    Returns:
    """

    
def create_image():