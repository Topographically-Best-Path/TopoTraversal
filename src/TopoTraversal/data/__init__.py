import TopoTraversal.constants as constants
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import pygmt
import csv
import os
import math

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
        frame=True
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
        annotation="1000+f6p",
        limit="-10000/10000",
        pen="a0.15p"
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

def get_etopo_data(lon, lat, size):
    '''
    PARAMETERS: -180 <= lon <= 180(suggested -175 <= lon <= 175),
                -89 <= lat <= 89(suggested -85 <= lat <= 85),
                0.05 <= size <= 90(suggested 0.1 <= size <= 10)
    RETURN VALUE: none
    REQUIREMENTS: none
    PURPOSE: creates Data.nc and Data.csv in the temp directory
    '''

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

    # creating temporary directory
    create_temp_dir()

    # extracting subregion and creating Data.nc file
    pygmt.grdcut(
        grid=topo_data,
        outgrid=constants.TEMPDIR/'Data.nc',
        projection='M4i',
        region=[minlon, maxlon, minlat, maxlat]
    )

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
