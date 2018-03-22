from shapely.geometry import Polygon, Point
from math import ceil, floor
import matplotlib.pyplot as plt
import math
import numpy as np



def get_mid_point(pt1, pt2, row):
    slope = (pt2[1] - pt1[1])/ (pt2[0] - pt1[0])
    return (row - pt1[1])*1/slope + pt1[0]


def search__bounds(polygon, left,right, lft_ind, rt_ind, cur_row, mid_point):
    l = polygon.contains(left)
    r = polygon.contains(right)

    lft_point = None
    rt_point = None
    if l and r:
        return left, right
    #left and right are not contained in the polygon
    else:
        #binary search
        #initialize midpoint, left pointer and right pointer
        mid_ = mid_point
        lft_ptr, rt_ptr = lft_ind, rt_ind
        while math.fabs(mid_ - lft_ptr) >= 0.5 or math.fabs(mid_ - rt_ptr) >= 0.5:
            Mid_point = Point(mid_, cur_row)
            if polygon.contains(Mid_point):
                rt_ptr = mid_
            else:
                lft_ptr = mid_
            mid_ = (lft_ptr + rt_ptr)/2
        lft_point = mid_
        mid_ = mid_point
        lft_ptr, rt_ptr = lft_ind, rt_ind
        while math.fabs(mid_ - rt_ptr) >= 0.5 or math.fabs(mid_ - lft_ptr) >= 0.5:
            Mid_point = Point(mid_, cur_row)
            if polygon.contains(Mid_point):
                lft_ptr = mid_
            else:
                rt_ptr = mid_
            mid_ = (lft_ptr + rt_ptr)/2
        rt_point = mid_

    return lft_point, rt_point



#the order of four points
def points_inside_polygon(polygon, pt1, pt2, pt3, pt4):

    coords_set = set(polygon.exterior.coords)
    centroid_x, centroid_y = polygon.centroid.x, polygon.centroid.y
    # print(centroid_x, centroid_y)
    print('fuckit')
    assert pt1 in coords_set and pt2 in coords_set and pt3 in coords_set and pt4 in coords_set

    pt_vector = np.array([pt1, pt2, pt3, pt4])
    max_y, min_y  = np.max(pt_vector[:,1]), np.min(pt_vector[:,1])
    max_x, min_x = np.max(pt_vector[:,0]), np.min(pt_vector[:,0])
    argmax_y, argmin_y = np.argmax(pt_vector[:,1]), np.argmin(pt_vector[:,1])
    argmax_x, argmin_x = np.argmax(pt_vector[:,0]), np.argmin(pt_vector[:,0])

    ret = []
    
    for row in range(min_y + 1, max_y):
        left = Point(min_x - 5, row)
        right = Point(max_x + 5, row)
        hori = row
        lft = min_x - 5
        rt = max_x + 5
        mid_point = None
        if row <= centroid_y:
            mid_point = get_mid_point(pt_vector[argmin_y], [centroid_x, centroid_y], row)
        else:
            mid_point = get_mid_point([centroid_x, centroid_y], pt_vector[argmax_y], row)

        start, end = search__bounds(polygon, left, right, lft, rt, hori, mid_point)
        start,end = int(start), int(end)
        if start >= end or mid_point == None:
            raise Exception('your polygon algorithm is fucked')

        for col in range(start, end+1):
            #col is latitude, row is longitude
            ret.append([col,row])

    return ret


def find_nearest_border(min_lon, max_lon, min_lat, max_lat):
    #extend the rectangle to integer points
    return [floor(min_lon), ceil(max_lon), floor(min_lat), ceil(max_lat)]
