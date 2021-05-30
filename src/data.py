from opensimplex import OpenSimplex
import pandas as pd
import xarray as xr
import numpy as np
import constants
import netCDF4
import pygmt
import math
import csv
import os

def create_temp_dir():
    '''
    PARAMETERS:   none
    RETURN VALUE: none
    REQUIREMENTS: none
    PURPOSE:      creates new temp directory for data and image storage
    '''

    # creating temporary directory
    if not os.path.exists(constants.TEMPDIR):
        os.makedirs(constants.TEMPDIR)

def create_image():
    '''
    PARAMETERS:   none
    RETURN VALUE: none
    REQUIREMENTS: Data.nc has to be created in the temp directory
    PURPOSE:      creates Image1.png in the temp directory
    '''

    # creating temporary directory
    create_temp_dir()

    # resetting figure
    constants.FIG = pygmt.Figure()

    # make color pallets
    pygmt.makecpt(
        cmap='topo',
        series='-10000/10000/500',
        continuous=True
    )

    # plotting topography data
    constants.FIG.grdimage(
        grid=str(constants.TEMPDIR/'Data.nc'),
        shading=True,
        frame=True,
        projection='M4i',
        region=get_bounds()
    )

    # plotting coastlines
    constants.FIG.coast(
        shorelines=True,
        frame=True
    )

    # plotting topo contour lines
    constants.FIG.grdcontour(
        grid=str(constants.TEMPDIR/'Data.nc'),
        interval=1000,
        annotation="2000+f6p",
        limit="-10000/10000",
        pen="a0.12p"
    )

    # creating color bar
    constants.FIG.colorbar(
        frame='+l" "'
    )

    # saving figure as Image.png
    constants.FIG.savefig(constants.TEMPDIR/"Image1.png", crop=False, dpi=720)

def plot_points(points):
    '''
    PARAMETERS:   points, [[x1,y1],[x2,y2],...] coordinates of points in the path
    RETURN VALUE: none
    REQUIREMENTS: Image2.png has be created in the temp directory
    PURPOSE:      creates Image3.png with path plotted
    '''

    # creating temporary directory
    create_temp_dir()

    # separating x and y coordinates
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    # resetting image
    plot_endpoints([x[0],y[0]],[x[-1],y[-1]])

    # plot data points
    constants.FIG.plot(
        x=x,
        y=y,
        style='c0.05c',
        color='white',
        pen='black',
    )

    # saving figure as Image.png
    constants.FIG.savefig(constants.TEMPDIR/"Image3.png", crop=False, dpi=720)

def plot_endpoints(start, end):
    '''
    PARAMETERS:   start, [x,y] coordinates of starting point
                  end, [x,y] coordinates of ending point
    RETURN VALUE: none
    REQUIREMENTS: Image1.png has be created in the temp directory
    PURPOSE:      creates Image2.png with endpoints plotted
    '''

    # creating temporary directory
    create_temp_dir()

    # resetting image
    create_image()

    # plot data points
    constants.FIG.plot(
        x=[start[0],end[0]],
        y=[start[1],end[1]],
        style='c0.2c',
        color='red',
        pen='black',
    )

    # saving figure as Image.png
    constants.FIG.savefig(constants.TEMPDIR/"Image2.png", crop=False, dpi=720)

def get_scale():
    '''
    PARAMETERS:   none
    RETURN VALUE: [londist, latdist, diagdist], distance between two lon points,
                  two lat points, and two diagonal points respectively
    REQUIREMENTS: Data.csv has to be created in the temp directory
    PURPOSE:      to get the distance between points, used in the algo
    '''

    # creating temporary directory
    create_temp_dir()

    # loading data from Data.csv
    arr = np.loadtxt(constants.TEMPDIR/"Data.csv", delimiter=',')
    lon = arr[:, 0]
    lat = arr[:, 1]
    alt = arr[:, 2]

    # finding indexs of the first repitition of data
    temp = np.where(lon == lon[0])
    index1 = temp[0][0]
    index2 = temp[0][1]

    # calculating londist, latdist, and diagdist in degrees
    londist = (lon[1] - lon[0])
    latdist = (lat[index2] - lat[index1])
    diagdist = math.sqrt(londist ** 2 + latdist ** 2)

    # converting degrees to meters and returning values
    londist = londist * 60 * 60 * 30
    latdist = latdist * 60 * 60 * 30
    diagdist = diagdist * 60 * 60 * 30
    return [londist, latdist, diagdist]

def convert_to_csv():
    '''
    PARAMETERS:   none
    RETURN VALUE: none
    REQUIREMENTS: Data.nc has to be created in the temp directory
    PURPOSE:      creates Data.csv in the temp directory
    '''

    # creating temporary directory
    create_temp_dir()

    # reading in data from Data.nc
    nc = xr.open_dataset(constants.TEMPDIR/'Data.nc')
    lon = nc.variables['x'][:]
    length = np.size(lon)
    lat = nc.variables['y'][:]
    width = np.size(lat)
    alt = nc.variables['z'][:]

    # reshaping and flattening data
    lon = np.tile(lon,width)
    lat = np.tile(lat,length)
    lat = np.reshape(lat,(width,length))
    lat = lat.flatten('F')
    alt = np.array(alt)
    alt = alt.flatten()

    # concatenating data together
    data = np.column_stack((lon,lat,alt))

    # creating Data.csv
    np.savetxt(constants.TEMPDIR/'Data.csv',data,delimiter=',')

def convert_to_nc():
    '''
    PARAMETERS:   none
    RETURN VALUE: none
    REQUIREMENTS: Data.csv has to be created in the temp directory
    PURPOSE:      creates Data.nc in the temp directory
    '''

    # creating temporary directory
    create_temp_dir()

    # reading in data from Data.csv
    arr = np.loadtxt(constants.TEMPDIR/"Data.csv", delimiter=',')
    lon = arr[:, 0]
    lat = arr[:, 1]
    alt = arr[:, 2]

    # extracting dimensions of lon, lat, and alt
    temp = np.where(lon == lon[0])
    index1 = temp[0][0]
    index2 = temp[0][1]
    londim = index2 - index1
    latdim =  int(np.shape(lat)[0] / londim)
    altdim = (londim, latdim)

    # rehaping lon, lat, and alt
    lon = lon[0:londim]
    lat = lat.reshape(londim, latdim)
    lat = lat[:, 0]
    alt = np.reshape(alt,(londim, latdim))

    # creating Data.nc and setting dimensions
    nc = netCDF4.Dataset(constants.TEMPDIR/'Data.nc','w','NETCDF4')
    nc.createDimension('x',londim)
    nc.createDimension('y',latdim)

    # adding data to Data.nc and closing the file
    lonvar = nc.createVariable('x','float32',('x'))
    lonvar[:] = lon
    latvar = nc.createVariable('y','float32',('y'))
    latvar[:] = lat
    altvar = nc.createVariable('z','float32',('x','y'));
    altvar[:] = alt;
    nc.close();

def get_etopo_data(lon, lat, size):
    '''
    PARAMETERS:   -180 <= lon <= 180(suggested -175 <= lon <= 175),
                  -89 <= lat <= 89(suggested -85 <= lat <= 85),
                  0.05 <= size <= 90(suggested 0.1 <= size <= 10)
    RETURN VALUE: none
    REQUIREMENTS: none
    PURPOSE:      creates Data.nc and Data.csv in the temp directory
    '''

    # creating temporary directory
    create_temp_dir()

    # creating region boundaries
    minlon, maxlon = max(-180,lon-size), min(180, lon+size) # -180 < lon < 180
    minlat, maxlat = max(-89,lat-size), min(89,lat+size) # -89 < lat < 89

    # determining which etopo data file to use
    if (size > 2):
        topo_data = '@earth_relief_30s' # 30 arc seconds between points
    elif (size > 0.4):
        topo_data = '@earth_relief_15s' # 15 arc seconds between points
    else:
        topo_data = '@earth_relief_03s' # 03 arc seconds between points

    # extracting subregion and creating Data.nc file
    pygmt.grdcut(
        grid=topo_data,
        outgrid=constants.TEMPDIR/'Data.nc',
        projection='M4i',
        region=[minlon, maxlon, minlat, maxlat]
    )

    # converting Data.nc to Data.csv
    convert_to_csv()

def get_bounds():
    '''
    PARAMETERS:   none
    RETURN VALUE: [minlon, maxlon, minlat, maxlat], min and max values of lon and lat
    REQUIREMENTS: Data.csv has to be created in the temp directory
    PURPOSE:      finds the bounds of the region from a data file
    '''

    # creating temporary directory
    create_temp_dir()

    # loading data from Data.csv
    arr = np.loadtxt(constants.TEMPDIR/"Data.csv", delimiter=',')
    lon = arr[:, 0]
    lat = arr[:, 1]
    alt = arr[:, 2]

    # finding values and returning them
    return [np.min(lon),np.max(lon),np.min(lat),np.max(lat)]


def get_ncfile(path):
    '''
    PARAMETERS:   path, the path to the file that is going to be read
    RETURN VALUE: none
    REQUIREMENTS: the .nc file has to have only 3 variables x, y, z
                  shape of x = n, shape of y = m, shape of z = (n,m)
    PURPOSE:      creates Data.nc and Data.csv in the temp directory
    '''

    # creating temporary directory
    create_temp_dir()

    # opening and the nc file and Data.csv in temp directory
    src = netCDF4.Dataset(path)
    dst = netCDF4.Dataset(constants.TEMPDIR/'Data.nc','w','netCDF4')

    # copying attributes
    for name in src.ncattrs():
        dst.setncattr(name, src.getncattr(name))

    # copying dimensions
    for name in src.dimensions:
        dst.createDimension(name, len(src.dimensions[name]))

    # copying all file data and closing file
    for name in src.variables:
        x = dst.createVariable(name, src.variables[name].datatype, src.variables[name].dimensions)
        dst.variables[name][:] = src.variables[name][:]
    src.close()
    dst.close()

    # converting Data.nc to Data.csv
    convert_to_csv()

    # setting up subregion for image creation
    pygmt.grdcut(
        grid=str(constants.TEMPDIR/'Data.nc'),
        outgrid=constants.TEMPDIR/'Data.nc',
        projection='M4i',
        region=get_bounds()
    )

def get_csvfile(path):
    '''
    PARAMETERS:   path, the path to the file that is going to be read
    RETURN VALUE: none
    REQUIREMENTS: the .csv file should be n rows and 3 columns with column 1 being
                  lon, column 2 being lat, column 3 being alt. lon should differ in
                  values before lat does
    PURPOSE:      creates Data.nc and Data.csv in the temp directory
    '''

    # creating temporary directory
    create_temp_dir()

    # opening and creating Data.csv
    arr = np.loadtxt(path,delimiter=',')
    np.savetxt(constants.TEMPDIR/'Data.csv',arr,delimiter=',')

    # converting Data.csv to Data.nc
    convert_to_nc()

    # setting up subregion for image creation
    pygmt.grdcut(
        grid=str(constants.TEMPDIR/'Data.nc'),
        outgrid=constants.TEMPDIR/'Data.nc',
        projection='M4i',
        region=get_bounds()
    )

def create_random_terrain(freq, height, water):
    '''
    PARAMETERS:   freq, 5 <= freq <= 25, controls how mountainy the data will be
                  height, 100 <= height <= 8000, controls max altitude difference
                  water, 0 <= water <= 100, percentage of the map that will be under water
    RETURN VALUE: none
    REQUIREMENTS: none
    PURPOSE:      creates Data.nc and Data.csv in the temp directory
    '''

    # creating temporary directory
    create_temp_dir()

    # initializing altitude data with noise generator
    n = 500
    gens = [OpenSimplex(seed=i) for i in range(10)]
    alt = np.zeros((n,n))
    for x in range(n):
        for y in range(n):
            for i,gen in enumerate(gens):
                alt[x][y] += (0.5**i)*(gen.noise2d(freq*(x/n-0.5), freq*(y/n-0.5)) / 2 + (0.5-water/100))
    alt *= height
    alt = alt.flatten()

    # creating lon and lat values
    lon = np.linspace(-2,2,n)
    lon = np.tile(lon,n)
    lat = np.linspace(-2,2,n)
    lat = np.tile(lat,n)
    lat = np.reshape(lat,(n,n))
    lat = lat.flatten('F')

    # concatenating data together
    data = np.column_stack((lon,lat,alt))

    # creating Data.csv
    np.savetxt(constants.TEMPDIR/'Data.csv',data,delimiter=',')

    # creating Data.nc
    convert_to_nc()

    # setting up subregion for image creation
    pygmt.grdcut(
        grid=str(constants.TEMPDIR/'Data.nc'),
        outgrid=constants.TEMPDIR/'Data.nc',
        projection='M4i',
        region=[-2,2,-2,2]
    )

def main():
    '''
    PARAMETERS:   none
    RETURN VALUE: none
    REQUIREMENTS: none
    PURPOSE:      runs all other functions in file at least once, to make sure
                  they are working. If this errors the data.py will fail
    '''

    # Test 1: Etopo Data Collection
    create_temp_dir()
    get_etopo_data(0,0,3)
    create_image()
    plot_endpoints([0.0,0.0],[2.0,0.0])
    plot_endpoints([-2.0,0.0],[0.0,0.0])
    plot_points([[i/120.0,-(i/120.0 - 1)**2 + 1] for i in range(0,241)])
    plot_points([[-i/120.0,-(-i/120.0 + 1)**2 + 1] for i in range(0,241)])
    print(get_bounds())
    print(get_scale())

    # Test 2: NC File Data Collection
    create_temp_dir()
    get_ncfile('TestData.nc')
    convert_to_csv()
    create_image()
    plot_endpoints([0.0,0.0],[2.0,0.0])
    plot_points([[i/120.0,-(i/120.0 - 1)**2 + 1] for i in range(1,240)])
    print(get_bounds())
    print(get_scale())

    # Test 3: CSV File Data Collection
    create_temp_dir()
    get_csvfile('TestData.csv')
    convert_to_nc()
    create_image()
    plot_endpoints([0.0,0.0],[2.0,0.0])
    plot_points([[i/120.0,-(i/120.0 - 1)**2 + 1] for i in range(1,240)])
    print(get_bounds())
    print(get_scale())

    # Test 4: Random Data Generation
    create_temp_dir()
    create_random_terrain(15, 4000, 50)
    create_image()
    plot_endpoints([0.0,0.0],[2.0,0.0])
    plot_points([[i/120.0,-(i/120.0 - 1)**2 + 1] for i in range(1,240)])
    print(get_bounds())
    print(get_scale())

if __name__ == "__main__":
    main()
