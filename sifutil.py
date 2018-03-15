import math
from math import sin, cos, sqrt
from pyproj import Proj, transform

WGS84 = 'epsg:4326'
CONUS_ALBERS = 'epsg:5069'

def haversine_dist(lon_a, lat_a, lon_b, lat_b):
    R = 6371
    dLat = deg2rad(lat_b - lat_a)
    dLon = deg2rad(lon_b - lon_a)
    a = (sin(dLat/2.) * sin(dLat/2)) +\
        cos(deg2rad(lat_a)) * cos(deg2rad(lat_b)) *\
        sin(dLon/2.) * sin(dLon/2.)
    c = 2 * math.atan2(sqrt(a), sqrt(1-a))
    d = R * c
    return d

def deg2rad(deg):
    return deg * (math.pi / 180.)

def convertProjection(x, y, from_crs, to_crs):
    inProj = Proj(init=from_crs)
    outProj = Proj(init=to_crs)
    x2, y2 = transform(inProj, outProj, x, y)
    return (x2, y2)

def invProjection(x, y, from_crs, to_crs):
	inProj = Proj(init = from_crs)
	outProj = Proj(init = to_crs)
	x1,y1 = outProj(x,y, inverse = True)
	print(x1,y1)


def within_bounds(loc, bounds):
    lon = loc[0]
    lat = loc[1]
    if (lat > bounds[0] and lat < bounds[2] and lon > bounds[1] and lon < bounds[3]):
        return True
    else:
        return False

def date_to_DOY(date):
    return date.timetuple().tm_yday