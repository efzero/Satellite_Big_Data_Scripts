
from shapely.geometry import Polygon
from helper import *
from pyhdf.SD import SD, SDC
from my_functions import *


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


  #input the path of the file of our fpar data
  #returns true if successfully read the data, else throw assertion
  def read_fpar(self, path):
    try:
      data = SD(path, SDC.READ)
      self.fpar = np.array(data.select('Fpar_500m')[:])
      self.qc = np.array(data.select('FparExtra_QC')[:])
      self._laiqc = np.array(data.select('FparLai_QC')[:])
      return True

    except:
      assert self.fpar != None and self.qc != None



  #get the fpar data indices inside a bounding box
  #input lb: left bottom, lu: left up, rb: right bottom , ru: right up coordinates
  #return the indices of fpar box
  def get_fpar_indices_by_box(self, lu, ru, rb, lb,  fpar_data):
    p1 = self.coords_to_ind(lu[0], lu[1])
    p2 = self.coords_to_ind(ru[0], ru[1])
    p3 = self.coords_to_ind(rb[0], rb[1])
    p4 = self.coords_to_ind(lb[0], lb[1])
    polygon = Polygon((p1, p2, p3, p4))
    indices = points_inside_polygon(polygon, p1, p2, p3, p4)

    return indices


  def coords_to_ind(self, lat, lon):

    """
    input latitude and longitude
    return the according indices on fpar grid
    """
    
    lon_diff = lon - self.west
    lat_diff = self.north - lat

    lon_ind = int(lon_diff / self.lon_interval * self.lon_num)
    lat_ind = int(lat_diff / self.lat_interval * self.lat_num)
    return (lat_ind, lon_ind)


  def get_fpar_coords(self, lat_ind, lon_ind):

    """
    input lat and lon indices on modis fpar data
    return the according latitude and longitude of that data
    """
 
    lat = self.north - lat_ind / self.lat_num * (self.north - self.south)
    lon = self.west + lon_ind / self.lon_num * (self.east - self.west)
    return (lon, lat)


  #input the lat and lon indices on modis data
  #output the four coordinates of that bounding box
  def get_fpar_box(self, lat_ind, lon_ind):
    try:
      lu = self.get_fpar_coords(lat_ind, lon_ind)
      lb = self.get_fpar_coords(lat_ind+1, lon_ind)
      ru = self.get_fpar_coords(lat_ind, lon_ind+1)
      rb = self.get_fpar_coords(lat_ind+1, lon_ind+1)
      return [lb, rb, ru, lu]
    except:
      assert False
      return None

  def get_fpar_bound(self, lat_ind, lon_ind):

    """
    args:lat index and lon index
    input:　lat index, lon index of the fpar data (left up corner)
    returns: the min_lon, max_lon, min_lat, max_lat of the corresponding bounding box of fpar


    """

    assert lat_ind >= 0 and lon_ind >= 0
    lu = self.get_fpar_coords(lat_ind, lon_ind)
    lb = self.get_fpar_coords(lat_ind+1, lon_ind)
    ru = self.get_fpar_coords(lat_ind, lon_ind+1)
    rb = self.get_fpar_coords(lat_ind+1, lon_ind+1)
    max_lat, min_lat = max(lu[1], lb[1]), min(lu[1], lb[1])
    max_lon, min_lon = max(lu[0], ru[0]), min(lu[0], ru[0])
    return [min_lon, max_lon, min_lat, max_lat]



  #input the indices of fpar data
  #return the corresponding fpar values and qc values
  #parameter: fpar_dat: the global fpar data, fpar_qc: the global qc data, indices: the corresponding indices
  def get_fpar_by_indices(self,fpar_dat, fpar_qc, indices):
    fp_values = []
    qc_values = []
    for i in range(len(indices)):
      row, col = indices[i, 0], indices[i, 1]
      fp_data = fpar_dat[row, col]
      fp_qc = fpar_qc[row, col]
      fp_values.append(fp_data)
      qc_values.append(fp_qc)

    return fp_values, qc_values



  def get_fpar_directedly(self, lo, hi, left, right):

    """
    @input the four borders of the fpar array
    @return the sliced fpar matrix

    """
    return self.fpar[lo:hi, left:right], self.qc[lo:hi, left:right], self._laiqc[lo:hi, left:right]

  
  def strong_filter_fpar(self, fpar, qc, laiqc):

    """
    @given fpar, extra qc and lai qc
    @return the filtered fpar

    Args: 
      fpar, qc, laiqc
    Returns:
      strongly filtered fpar, missing value filled with -1  

    """
    ret = np.zeros(fpar.shape)
    for i in range(qc.shape[0]):
      for j in range(qc.shape[1]):
        lai_qc_info = convert_binary(laiqc[i,j])
        extra_qc_info = convert_binary(qc[i,j])[1:]

        if lai_qc_info == '00000000' and (extra_qc_info == '0000000' or extra_qc_info == '0001000'):
          ret[i,j] = fpar[i,j]

        else:
          ret[i,j] = np.NaN

    return ret




























