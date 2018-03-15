from FPAR_utils import *
from CDL_utils import *


def test_io():
    path_1 = '../sif_data/2016113.hdf'
    fp = fpar_utils()
    fp.read_fpar(path_1)
    print('testing fpar')
    print(fp.fpar.shape)
    print(fp.qc.shape)


    path_2 = '../sif_data/CDL.tif'
    cdl = cdl_utils()
    dat = cdl.load_cdl(path_2)
    print('testing cdl')
    print(dat.shape)

    print('testing saving cdl')

    cdl.save_cdl()
    arr = np.load('cdl.npy')
    print(arr.shape)
    return





def test_projection():
    fp = fpar_utils()
    cdl = cdl_utils()

    projection = cdl.getCDLprojection(-88, 40)
    # print(cdl.getCDLprojection(-88, 40))
    print(cdl.proj_to_ind(projection))

    projection1 = cdl.getCDLprojection(-91.75, 41.70)
    projection2 = cdl.getCDLprojection(-91.98, 37.49)
    projection3 = cdl.getCDLprojection(-86.10, 41.42)
    projection4 = cdl.getCDLprojection(-86.65, 37.21)

    print(cdl.proj_to_ind(projection1))
    print(cdl.proj_to_ind(projection2))
    print(fp.coords_to_ind(50, -124.45))
    #1,0

    print(fp.coords_to_ind(30, -124.45))
    #3678,0


    print(fp.coords_to_ind(30, -69.27))
    #10145, 3678
    print(fp.coords_to_ind(50, -69.27))

# p1 = (38, -90)
# p2 = (39, -89)
# p3 = (37, -89.5)
# p4 = (36, -90.5)


# print(fp.get_fpar_indices_by_box(p1, p2, p3, p4, 0))

# pts = np.array(fp.get_fpar_indices_by_box(p1, p2, p3, p4, 0))

# plt.plot(pts[:,0], pts[:,1])
# plt.savefig('fpar.png')

test_projection()