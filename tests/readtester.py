import sys
sys.path.insert(1, '../src/')

import TopoTraversal.algo as algo
import TopoTraversal.gui as gui
import TopoTraversal.data as data

def main():
    data.create_temp()
    [x,y,z] = data.generate_large_data(40,285,5,5)
    data.generate_image(x,y,z)
    print(algo.get_path((43.8041, 282.8583), (43.8041, 285.5417), data.get_scale(5,5)[0], 0.25))

if __name__ == "__main__":
    main()