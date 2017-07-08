from objfileprocessing import objbased_normalized_mesh
from adaptive2Dgrid import adaptive2Dgrid
import geometry
from sys import argv
import numpy as np
from matplotlib import pyplot as plt
import threading as thr
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
#for i in range(height):
#    for j in range(width):
#        samplingpoint = ((j/width)*mesh.xspan, (i/height)*mesh.yspan)
#        containing_faces = grid.find(samplingpoint)3
#        if containing_faces:
#            sampleheight = max([geometry.calcMeshHeightFor2DPoint(samplingpoint, face) for face in containing_faces])
#            result.itemset((i,j), sampleheight)
#        # if no faces found, result at (x,y) remains 0

def thread_target(first, total, height, width):
    for position in range(first, first+total):
        i = int(floor(position / width))
        j = position % width
        samplingpoint = ((j / width) * mesh.xspan, mesh.yspan - (i / height) * mesh.yspan)
        containing_faces = grid.find(samplingpoint)
        if containing_faces:
            sampleheight = max([geometry.calcMeshHeightFor2DPoint(samplingpoint, face) for face in containing_faces])
            result.itemset(position, sampleheight)

total_samples = height * width
samples_per_thread = int(ceil(total_samples / nthreads))
threads = []
for k in range(nthreads-1):
    curr_thread = thr.Thread(target=thread_target, args=(k*samples_per_thread, samples_per_thread, height, width))
    threads.append(curr_thread)
    curr_thread.start()

total_so_far = (nthreads-1)*samples_per_thread
last_thread = thr.Thread(target=thread_target, args=(total_so_far, total_samples-total_so_far, height, width))
threads.append(last_thread)
last_thread.start()

for t in threads:
    t.join()

plt.imshow(result)
plt.colorbar()
plt.show()