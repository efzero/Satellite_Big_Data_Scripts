
from shapely.geometry import Polygon
from helper import *
from pyhdf.SD import SD, SDC


class fpar_utils:

  def __init__(self):

    self.west = -124.457906126032
    self.east = -69.2724108461701
    self.north = 50.0000009955098
    self.south = 30.0000009964079
    self.lat_num = 3678
    self.lon_num = 10145
    self.lon_interval = self.east - self.west
    self.lat_interval = self.north - self.south
    self.fpar = None
    self.qc = None

  #get the fpar data indices inside a bounding box
  #input lb: left bottom, lu: left up, rb: right bottom , ru: right up coordinates
  #return the indices of fpar box



  def read_fpar(self, path):
    try:
      data = SD(path, SDC.READ)
      self.fpar = data.select('Fpar_500m')[:]
      self.qc = data.select('FparExtra_QC')[:]
      return True

    except:
      assert self.fpar != None and self.qc != None



  def get_fpar_indices_by_box(self, lu, ru, rb, lb,  fpar_data):
    p1 = self.coords_to_ind(lu[0], lu[1])
    p2 = self.coords_to_ind(ru[0], ru[1])
    p3 = self.coords_to_ind(rb[0], rb[1])
    p4 = self.coords_to_ind(lb[0], lb[1])

    print(p1)
    polygon = Polygon((p1, p2, p3, p4))
    indices = points_inside_polygon(polygon, p1, p2, p3, p4)

    return indices


  #input latitude and longitude
  #return the according indices
  def coords_to_ind(self, lat, lon):
    lon_diff = lon - self.west
    lat_diff = self.north - lat

    print(lon_diff, lat_diff)
    lon_ind = int(lon_diff / self.lon_interval * self.lon_num)
    lat_ind = int(lat_diff / self.lat_interval * self.lat_num)
    return (lon_ind, lat_ind)



  #input lat and lon indices on modis data
  #return the according latitude and longitude 

  def get_fpar_coords(self, lat_ind, lon_ind):
    
    lat = self.north - lat_ind / self.lat_num * (self.north - self.south)
    lon = self.west + lon_ind / self.lon_num * (self.east - self.west)
    return (lon, lat)


  #input the lat and lon indices on modis data
  #output the four coordinates of that bounding box
  def get_fpar_box(self, lat_ind, lon_ind):
    try:
      lu = self.get_fpar_coords(lat_ind, lon_ind)
      lb = self.get_fpar_coords(lat_ind-1, lon_ind)
      ru = self.get_fpar_coords(lat_ind, lon_ind+1)
      rb = self.get_fpar_coords(lat_ind-1, lon_ind+1)
      return [lb, rb, ru, lu]

    except:
      return None


















