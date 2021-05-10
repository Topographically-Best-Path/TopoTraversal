import TopoTraversal.constants as constants
import os

def write_data(to_write:str) -> None:
    if not os.path.exists(constants.TEMPDIR):
        os.makedirs(constants.TEMPDIR)
    with open(constants.TEMPDIR / "temp.txt", "w") as fout:
        fout.write(to_write)
