from FPAR_utils import *
from CDL_utils import *



#testing reading fpar and cdl files from disk
def test_io():
    path_1 = 'FPAR_A2016241.hdf'
    fp = fpar_utils()
    fp.read_fpar(path_1)
    print('testing fpar')
    print(fp.fpar.shape)
    print(fp.qc.shape)

    #cdl_io

    # path_2 = '../sif_data/CDL.tif'
    # cdl = cdl_utils()
    # dat = cdl.load_cdl(path_2)
    # print('testing cdl')
    # print(dat.shape)

    # print('testing saving cdl')

    # cdl.save_cdl()
    # arr = np.load('cdl.npy')
    # print(arr.shape)
    return fp.fpar, fp.qc


#testing all projection functions of fpar and cdl
def test_projection():
    fp = fpar_utils()
    cdl = cdl_utils()

    projection = cdl.getCDLprojection(-88, 40)
    # print(cdl.getCDLprojection(-88, 40))
    print(cdl.proj_to_ind(projection))

    projection1 = cdl.getCDLprojection(-91.75, 41.70)
    projection2 = cdl.getCDLprojection(-91.75, 37.49)
    projection3 = cdl.getCDLprojection(-86.65, 41.70)
    projection4 = cdl.getCDLprojection(-86.65, 37.49)

    print(cdl.proj_to_ind(projection1))
    print(cdl.proj_to_ind(projection2))
    print(fp.coords_to_ind(50, -124.45))
    #1,0
    print(fp.coords_to_ind(30, -124.45))
    #3678,0
    print(fp.coords_to_ind(30, -69.27))
    #10145, 3678
    print(fp.coords_to_ind(50, -69.27))



#testing the bounding box algorithm
def test_fpar_box():

	fp = fpar_utils()
	cdl = cdl_utils()

	p4 = (39.86067026099156,-88.4386962890625)
	p3 = (39.86067026099156, -87.93082275390625)
	p2 = (40.38638178482896,-87.93082275390625)
	p1 = (40.38638178482896, -88.4386962890625)

	l = fp.get_fpar_indices_by_box(p1, p2, p3, p4, 0)
	s = set()
	for i in l:
		s.add((i[0], i[1]))
	pts = np.array(fp.get_fpar_indices_by_box(p1, p2, p3, p4, 0))
	print('set', len(s))
	print('list', len(l))
	# plt.plot(pts[:,0], pts[:,1])
	# plt.savefig('fpar.png')
	return pts

#testing whether the fpar corners are correct
def test_fpar_corners():
	fpar_dat, fpar_qc = test_io()
	fp = fpar_utils()
	indices = test_fpar_box()
	print(indices[0])
	print(fpar_dat[2287, 6299])

	fps, qcs = fp.get_fpar_by_indices(fpar_dat, fpar_qc, indices)
	print(len(fps))
	fp_corners = fp.get_fpar_box(indices[-1,0], indices[-1,1])
	print(fp_corners)
	return fp_corners



#input the latitude index and longitude index
#return the fpar grid point
def test_fp_corners(lat_ind, lon_ind):
	fp = fpar_utils()
	fpar_grid = fp.get_fpar_box(lat_ind, lon_ind)
	startpoint, endpoint = fp.get_fpar_box(0,0), fp.get_fpar_box(fp.lat_num-1, fp.lon_num -1)
	assert startpoint[3][0] - fp.west <= 0.0005 and startpoint[3][1] - fp.north <= 0.0005
	assert endpoint[0][0] - fp.east <= 0.0005 and endpoint[0][1] - fp.south <= 0.0005
	return fpar_grid


#testing whether cdl box is correct
def test_cdl_indices():
	fp_corners = test_fpar_corners()
	cdl = cdl_utils()

	#89.3, 38
	cdl.get_cdl_indices(fp_corners[0], fp_corners[1], fp_corners[2], fp_corners[3])
	cdl_data = np.load()


def test_fp_bound(lat_ind, lon_ind):
	fp = fpar_utils()
	box = fp.get_fpar_bound(lat_ind, lon_ind)
	startpoint, endpoint = fp.get_fpar_bound(0,0), fp.get_fpar_bound(fp.lat_num-1, fp.lon_num -1)
	print(startpoint, endpoint)
	assert startpoint[0] - fp.west <= 0.0005 and startpoint[3] - fp.north <= 0.0005
	assert endpoint[1] - fp.east <= 0.0005 and endpoint[2] - fp.south <= 0.0005
	return box

# print(test_fp_bound(2000, 5000))
# pts = test_fpar_box()
# fpar_, fpar_qc = test_io()
# fp = fpar_utils()

# fp, qc = fp.get_fpar_by_indices(fpar_, fpar_qc, pts)
# print(len(fp))
# print(len(pts[:,0]))


# print('shape', np.array(fp).shape)
# # plt.scatter(pts[:,0], pts[:,1], c = np.array(fp)/255)
# # plt.savefig('champaign.png')
# plt.figure()
# plt.scatter([1,2,3], [2,3,4])
# plt.savefig('scattermade.png')		