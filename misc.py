import math
from matplotlib import collections as mc, pyplot as plt

def triangles2SegmentLineCollection(triangles):
    triangleSegmentsToFlatten = [[[t[0], t[1]], [t[0], t[2]], [t[1], t[2]]] for t in triangles]
    triangleSegments = [segment for sublist in triangleSegmentsToFlatten for segment in sublist]
    return mc.LineCollection(triangleSegments, linewidths=1)

def plotTriangles(triangles, ax):
    lc = triangles2SegmentLineCollection(triangles)
    ax.add_collection(lc)
    ax.autoscale()

def nextPowerOfTwo(x):
    return 2 ** ( math.floor( math.log2(x) ) + 1 )

def findMaxTriangle2DSide(ts):
    dist = lambda p1, p2: math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )
    return max( [ max([dist(t[0], t[1]), dist(t[0], t[2]), dist(t[1], t[2])]) for t in ts ] )
    # max(ts, key=lambda t: max([dist(t[0], t[1]), dist(t[0], t[2]), dist(t[1], t[2])]))
