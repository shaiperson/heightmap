import multiprocessing as mp
import numpy as np
import geometry


def height4position(i, j, mesh):
    samplingpoint = ((j / shared_width.value) * mesh.xspan, mesh.yspan - (i / shared_height.value) * mesh.yspan)
    containing_faces = mesh.faces_for_2D_point(samplingpoint)
    if containing_faces:
        return max([geometry.calcMeshHeightFor2DPoint(samplingpoint, face) for face in containing_faces])
    else:
        return 0

def create(mesh, width, height, nprocs):

    global shared_width
    global shared_height

    shared_width = mp.Value('i', width)
    shared_height = mp.Value('i', height)

    arguments = [(i, j, mesh) for i in range(shared_height.value) for j in range(shared_width.value)]

    pool = mp.Pool(nprocs)
    result_list = list(pool.starmap_async(height4position, arguments).get())
    pool.close()
    pool.join()

    result_matrix = [ result_list[i*width:(i+1)*width] for i in range(height) ]

    return result_matrix