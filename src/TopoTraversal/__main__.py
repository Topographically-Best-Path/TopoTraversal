import TopoTraversal.gui as gui
import TopoTraversal.data as data

def main():
    data.create_temp()
    [x,y,z] = data.generate_large_data(40,285,5,5)
    print(data.get_scale(5,5))
    data.generate_image(x,y,z)

if __name__ == "__main__":
    main()
