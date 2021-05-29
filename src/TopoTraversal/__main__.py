import TopoTraversal.gui as gui
import TopoTraversal.data as data

def main():
    data.get_etopo_data(0,0,3)
    data.create_image()
    data.plot_endpoints([0.0,0.0],[2.0,0.0])
    data.plot_points([[i/120.0,-(i/120.0 - 1)**2 + 1] for i in range(1,240)])

if __name__ == "__main__":
    main()
