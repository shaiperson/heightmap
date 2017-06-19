import sys
import pylab as pl
from matplotlib import pyplot as plt

import objproc
import misc
import geometry
from adaptivegrid import adaptivegrid

def readInput():
    # vs3D, fs3D, xmax, ymax, zmax = objproc.readAndNormalizeMesh(sys.argv[3])
    return objproc.readAndNormalizeMesh(sys.argv[3])

def createGrid(faces, xmax, ymax, zmax):
    g = adaptivegrid((0, ymax), max(xmax, max(ymax, zmax)), 100)
    for t in faces:
        g.insert(t)
    return g

def plotTheThings(axis, fs3D, grid, heights, zmax):
    # plot triangles
    fs2D = [ (p0[:2], p1[:2], p2[:2]) for (p0, p1, p2) in fs3D ]
    misc.plotTriangles(fs2D, axis)

    # plot grid
    grid.plot(axis, 'k')

    # plot heightmap
    red = [1, 0, 0, 1]
    scaleHeightGreen = lambda zval: [0, zval/zmax, 0, 1]

    xs = [t[0] for t in heights]
    ys = [t[1] for t in heights]
    cs = [scaleHeightGreen(t[2]) if t[2] > -1 else red for t in heights]
    plt.scatter(xs, ys, facecolors=cs)


def createHeatmap(grid, xmax, ymax, hpoints, vpoints):
    xstep = xmax / hpoints
    ystep = ymax / vpoints

    result = []

    planePoints = [(r * xstep, s * ystep) for r in range(hpoints+1) for s in range(vpoints+1)]
    for point in planePoints:
        # print(point)
        x, y = point[0], point[1]
        triangles = grid.find(point)
        if triangles:
            heights = list(map(lambda t: geometry.calcMeshHeightFor2DPoint(point, t), triangles))
            result.append((x, y, max(heights)))
        else:
            sys.stderr.write("grid fail\n")
            result.append((x, y, -1))

    return result

vertices, faces, xmax, ymax, zmax = readInput()
grid = createGrid(faces, xmax, ymax, zmax)
heatmapPoints = createHeatmap(grid, xmax, ymax, int(sys.argv[1]), int(sys.argv[2]))

fig, ax = pl.subplots()
plotTheThings(ax, faces, grid, heatmapPoints, zmax)
plt.show()
