from objfileprocessing import objbased_normalized_mesh
from adaptive2Dgrid import adaptive2Dgrid
import geometry
from sys import argv
import numpy as np
from matplotlib import pyplot as plt
from threading import Thread
from math import ceil, floor

ADAPTIVE_2D_GRID_THRESHOLD = 100

# read command line arguments
width = int(argv[1])
height = int(argv[2])
objfile = argv[3]
nthreads = int(argv[4])
# read .obj file into mesh object and into a quadtree-based 2D adaptive grid
mesh = objbased_normalized_mesh(objfile)
grid = adaptive2Dgrid( (0, mesh.yspan), max(mesh.xspan, mesh.yspan),  ADAPTIVE_2D_GRID_THRESHOLD)
for f in mesh.faces:
    grid.insert(f)

# sample mesh into a height heatmap using the adaptive grid for efficient lookups
result = np.zeros((height, width))
for i in range(height):
    for j in range(width):
        samplingpoint = ((j/width)*mesh.xspan, (i/height)*mesh.yspan)
        containing_faces = grid.find(samplingpoint)
        if containing_faces:
            sampleheight = max([geometry.calcMeshHeightFor2DPoint(samplingpoint, face) for face in containing_faces])
            result.itemset((i,j), sampleheight)
        # if no faces were found, result at (i,j) remains 0

plt.imshow(result)
plt.colorbar()
plt.show()