import sys
sys.path.insert(1, '../src/')

import TopoTraversal.data as data

def main():
    # Test 1: Etopo Data Collection
    data.create_temp_dir()
    data.get_etopo_data(0,0,3)
    data.create_image()
    data.plot_endpoints([0.0,0.0],[2.0,0.0])
    data.plot_points([[i/120.0,-(i/120.0 - 1)**2 + 1] for i in range(1,240)])
    print(data.get_bounds())
    print(data.get_scale())

    # Test 2: NC File Data Collection
    data.create_temp_dir()
    data.get_ncfile('Data.nc')
    data.convert_to_csv()
    data.create_image()
    data.plot_endpoints([0.0,0.0],[2.0,0.0])
    data.plot_points([[i/120.0,-(i/120.0 - 1)**2 + 1] for i in range(1,240)])
    print(data.get_bounds())
    print(data.get_scale())

    # Test 3: CSV File Data Collection
    data.create_temp_dir()
    data.get_csvfile('Data.csv')
    data.convert_to_nc()
    data.create_image()
    data.plot_endpoints([0.0,0.0],[2.0,0.0])
    data.plot_points([[i/120.0,-(i/120.0 - 1)**2 + 1] for i in range(1,240)])
    print(data.get_bounds())
    print(data.get_scale())

    # Test 4: Random Data Generation
    data.create_temp_dir()
    data.create_random_terrain(15, 4000, 50)
    data.create_image()
    data.plot_endpoints([0.0,0.0],[2.0,0.0])
    data.plot_points([[i/120.0,-(i/120.0 - 1)**2 + 1] for i in range(1,240)])
    print(data.get_bounds())
    print(data.get_scale())

if __name__ == "__main__":
    main()
