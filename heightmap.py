import multiprocessing as mp
import numpy as np
import geometry


def height4position(i, j, mesh):
    samplingpoint = ((j / shared_width.value) * mesh.xspan, mesh.yspan - (i / shared_height.value) * mesh.yspan)
    containing_faces = mesh.faces_for_2D_point(samplingpoint)
    if containing_faces:
        candidates = [geometry.calcMeshHeightFor2DPoint(samplingpoint, face) for face in containing_faces]
        result = max(candidates)
        return result
    else:
        return 0

def create(mesh, width, height, nprocs):

    global shared_width
    global shared_height

    shared_width = mp.Value('i', width)
    shared_height = mp.Value('i', height)

    subregion_row = 59
    subregion_col = 521
    subwidth = 8
    subheight = 8

    # arguments = [(i, j, mesh) for i in range(shared_height.value) for j in range(shared_width.value)]
    arguments = [(i, j, mesh) for i in range(subregion_row, subregion_row + subheight) for j in range(subregion_col, subregion_col + subwidth)]

    pool = mp.Pool(nprocs)
    result_list = list(pool.starmap_async(height4position, arguments).get())
    pool.close()
    pool.join()

    # result_matrix = [ result_list[i*width:(i+1)*width] for i in range(height) ]
    result_matrix = [ result_list[i*subwidth:(i+1)*subwidth] for i in range(subheight) ]

    return result_matrix