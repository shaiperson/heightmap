import multiprocessing as mp
import numpy as np
import geometry

def height4position(i, j, mesh):
    samplingpoint = ((j / shared_width.value) * mesh.xspan, mesh.yspan - (i / shared_height.value) * mesh.yspan)
    containing_faces = mesh.faces_for_2D_point(samplingpoint)
    if containing_faces: # Faces were found that enclose (i,j)
        candidates = [geometry.calcMeshHeightFor2DPoint(samplingpoint, face) for face in containing_faces] # Folds in the mesh mean more than one candidate
        result = max(candidates)
        return result
    else: # Point (i,j) falls within a mesh hole
        return 0

def create(mesh, width, height, nprocs):

    global shared_width
    global shared_height

    shared_width = mp.Value('i', width)
    shared_height = mp.Value('i', height)

    arguments = [(i, j, mesh) for i in range(height) for j in range(width)]

    pool = mp.Pool(nprocs)
    result_list = list(pool.starmap_async(height4position, arguments).get())
    pool.close()
    pool.join()

    result_matrix = [ result_list[i*width:(i+1)*width] for i in range(height) ]

    return np.array(result_matrix)
