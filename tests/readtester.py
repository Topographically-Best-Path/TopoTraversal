import sys
sys.path.insert(1, '../src/')

import TopoTraversal.algo as algo
import TopoTraversal.gui as gui
import TopoTraversal.data as data

def main():
    data.create_temp_dir()
    data.get_etopo_data(40,285,5)
    data.create_image()
    print(algo.get_path((43.8041, 282.8583), (43.8041, 285.5417), data.get_scale()[0], 0.25))

if __name__ == "__main__":
    main()
