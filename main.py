from objfileprocessing import objbased_normalized_mesh
import matplotlib
matplotlib.use('Agg')
import sys
from matplotlib import pyplot as plt
from time import time
import heightmap

######### READING MESH FILE #########

# read command line arguments
objfile = sys.argv[1]

# read .obj file into mesh object
print('Reading mesh from file...')
reading_start = time()
mesh = objbased_normalized_mesh(objfile)
reading_end = time()

print('Done! Reading time', reading_end - reading_start, '\n')

######### CREATING HEIGHT MAPS #########

# TODO: handle SIGINT to support correcting interactive input in runtime

width = height = nthreads = filename = None # for greater IDE happiness
colormap = 'viridis'
while True:
    width = input('Map width: ') or width
    height = input('Map height: ') or height
    nthreads = input('Number of threads: ') or nthreads
    filename = input('Result file: ') or filename
    colormap = input('Pyplot colormap (\'viridis\' by default): ') or colormap

    print('Processing...')

    try:
        processing_start = time()
        image = heightmap.create(mesh, int(width), int(height), int(nthreads))
        processing_end = time()
    except:
        print('An error occurred, try again', '\n')
        continue

    print('Done! Processing time', processing_end - processing_start, '\n')

    plt.imshow(image)
    plt.colorbar()
    plt.imsave(filename, image)
    # plt.show()
