import sifutil
import numpy as np
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
import numpy as np
# from mpl_toolkits.basemap import Basemap, cm
import math
from math import sin, cos, sqrt
from pyproj import Proj, transform
# requires netcdf4-python (netcdf4-python.googlecode.com)
# from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt
from io import StringIO
BASE_CDL_URL = 'https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLStat'
CHAMPAIGN = 17019

COORD_INC = 20/3678.
LEFT = -124.45790626020
RIGHT = -69.277252174347
UPPER = 49.999999995507
LOWER = 29.994633289321


def convert_binary(num):
    str_ = "{0:b}".format(num)
    if len(str_) < 8:
        str_ = '0'*(8-len(str_)) + str_
        
    return str_
        
def get_cloud(num):
    str_ = convert_binary(num)
    return str_[1], str_[2]


def interpolation(x,y):
    x = np.array(x)
    matrix = np.array([x**i for i in range(len(x))]).transpose()
    print(matrix)
    coeffs = la.solve(matrix,y)
    return coeffs

def get_smooth_line(x,y):
    coeffs = interpolation(x,y)
    x_values = np.linspace(min(x), max(x), 100)
    y_values = []
    for i in x_values:
        value = 0
        for j in range(len(coeffs)):
            value += coeffs[j]*i**j
            
        y_values.append(value)
    return [list(x_values), y_values]

def clean_data(time_series, x_values, qc):
    good_fpars = []
    good_dates = []
    for i in range(len(time_series)):
        if get_cloud(qc[i])[0] == '0' and get_cloud(qc[i])[1] == '0':
            good_fpars.append(time_series[i])
            good_dates.append(x_values[i])
        
    return good_dates, good_fpars

def good_qc(qc):
    cnt = 0
    for i in range(len(qc)):
        if get_cloud(qc[i])[0] == '0' and get_cloud(qc[i])[1] == '0':
            cnt += 1
            
    return cnt/len(qc)


def coords_to_ind(lon, lat):
    lon_diff = lon - LEFT
    lat_diff = UPPER - lat
    lon_ind = int(lon_diff / COORD_INC)
    lat_ind = int(lat_diff / COORD_INC)
    return (lon_ind, lat_ind)

def hasdf():
    print('shabi')

def get_by_box(year, llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat):
    from io import StringIO
    x1, y1 = sifutil.convertProjection(llcrnrlon, llcrnrlat, sifutil.WGS84, sifutil.CONUS_ALBERS)
    x2, y2 = sifutil.convertProjection(urcrnrlon, urcrnrlat, sifutil.WGS84, sifutil.CONUS_ALBERS)

    print(x1,y1)
    # url = BASE_CDL_URL + '?year=' + str(year) + '&bbox=' + str(min(x1,x2)) + "," +\
    #       str(min(y1, y2)) + "," + str(max(x1, x2)) + "," + str(max(y1, y2)) + "&format=csv"
    # # print(url)
    # # print('loldashabi   ')

    # with warnings.catch_warnings():
    #     warnings.simplefilter("ignore")
    #     res = requests.get(url, verify = False)
    #     returnurl = BeautifulSoup(res.text, 'lxml').find('returnurl').text
    # print(returnurl)
    # with warnings.catch_warnings():
    #     rawdata = requests.get(returnurl, verify = False).text
    # raw_iter = StringIO(rawdata)
    # df = pd.read_csv(raw_iter, sep=" *, * ")\
    #    .apply(pd.to_numeric, errors='ignore')\
    #    .set_index("Category")
    # return df 


def get_fractions(cdl):
    total_acre = sum(cdl['Acreage'])
    if total_acre == 0:
        corn = 0
        soy = 0
        forest = 0
        grass = 0
        return
    if "Corn" in cdl.index:
        corn = cdl['Acreage']['Corn'] / total_acre
    else:
        corn = 0
    if "Soybeans" in cdl.index:
        soy = cdl['Acreage']['Soybeans'] / total_acre
    else:
        soy = 0
    pattern = re.compile(r' Forest')
    trees = [cdl.index[i] for i in range(len(cdl.index))\
             if re.search(pattern, cdl.index[i]) != None]
    frst = 0
    for tree in trees:
        frst += cdl['Acreage'][tree]
    forest = frst /  total_acre
    grass = 1 - (forest + corn + soy)
    return  np.array([corn, soy, forest, grass])





def fparreg_workflow():
    big_mat = get_proportion_matrix()
#     rhs = get_fpars('FPAR_A2016361.hdf')
    print(big_mat)
    save_matrix(big_mat)
    mat = load_matrix('dajuzhen2.npy')
    print(mat)
    
    
def get_proportion_matrix():
    from my_functions import get_fractions, get_by_box
    mat2 = np.zeros((16,4))
    base_lat, base_lon = 38.3, -89.59
    
    
    base_lat = 40.7
    base_lon = -88.2
    row = 0 
    
    for i in range(4):
        cur_lon = base_lon
        for j in range(4):
            print(base_lat, cur_lon)
            mat2[row,:] = get_fractions(get_by_box(2016, cur_lon - 0.01, base_lat, cur_lon, base_lat + 0.01))
            cur_lon -= 0.01
            print(row)
            row += 1
        base_lat += 0.01
    return mat2    
    
    
def get_processed_matrix_and_rhs(mat, rhs):
    indices = []
    for i in range(len(rhs)):
        if rhs[i] != 0:
            indices.append(i)
    indices = np.array(indices)
#     print(indices)
    return mat[indices, :], rhs[indices]


def save_matrix(mat):
    from tempfile import TemporaryFile
    outfile = TemporaryFile()
    np.save('dajuzhen.npy', mat)
    
    
    
def load_matrix(file):
    return np.load(file)



def run_regression():
    from my_functions import get_cloud, coords_to_ind
    from scipy.optimize import lsq_linear

    time_series = np.zeros((4, 45))
    ct = 0
    x_values = []    
    
    prefix ='FPAR_A2016'
    suffix = '.hdf'
    ct = 0

#     print(prefix+suffix)

    for i in range(1,361,8):
        a = str(int(i))
        if i < 10:
            a = '00'+ a
        elif i < 100:
            a = '0' + a

        query = prefix + a + suffix
#         print(query)
        try:
            data = SD(query, SDC.READ)
            m2 = load_matrix('dajuzhen.npy')
            rhs = get_fpars(query)
#             print(rhs)
            mat2, rhs2 = get_processed_matrix_and_rhs(m2,rhs)
            
#             print(mat2)
            
#             result = np.linalg.lstsq(mat2,rhs2)
#             print(result[0])
            
            result = lsq_linear(mat2, rhs2, bounds = (0, 100))
#             print(result.x)
#             print('result', result[0])
            ct += 1
# #             print('result', result[0])
            time_series[:,ct-1] = np.array(result.x)
            x.append(i)
                 
        except Exception as e:
            print(e)
            continue
                 
    return x_values, time_series



def convertProjection(x, y, from_crs, to_crs):
    inProj = Proj(init=from_crs)
    outProj = Proj(init=to_crs)
    x2, y2 = transform(inProj, outProj, x, y)
    return (x2, y2)


def getCDLprojection(lon,lat):

    return sifutil.convertProjection(lon, lat, sifutil.WGS84, sifutil.CONUS_ALBERS)

def getInverseProj(x,y):
    return sifutil.invProjection(x,y, sifutil.WGS84, sifutil.CONUS_ALBERS)