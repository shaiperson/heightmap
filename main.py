from objfileprocessing import objbased_normalized_mesh
from sys import argv
from matplotlib import pyplot as plt
from time import time
import heightmap

# read command line arguments
objfile = argv[1]

# read .obj file into mesh object
reading_start = time()
mesh = objbased_normalized_mesh(objfile)
reading_end = time()

print('reading time', reading_end - reading_start)

width = height = nthreads = filename = None # for greater IDE happiness
while True:
    width = input('Map width: ') or width
    height = input('Map height: ') or height
    nthreads = input('Number of threads: ') or nthreads
    filename = input('Result file: ') or filename

    processing_start = time()
    image = heightmap.create(mesh, int(width), int(height), int(nthreads))
    processing_end = time()


    print('\n', 'Done! Processing time', processing_end - processing_start, '\n')

    plt.imshow(image)
    plt.colorbar()
    plt.imsave(filename, image)
    # plt.show()