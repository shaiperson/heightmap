import numpy as np
from matplotlib import collections as mc

import geometry

# threshold should be such that no grid cell falls within a triangle
class adaptive2Dgrid:

    data = []
    count = 0
    leaf = True

    tlcorner = None
    size = 0

    upperleft = None
    upperright = None
    lowerleft = None
    lowerright = None

    def __init__(self, tlcorner, size, threshold):
        self.tlcorner = tlcorner
        self.size = size
        self.threshold = threshold
        self.data = []

    def __eq__(self, other):
        return self.tlcorner == other.tlcorner and self.size == other.size

    def __hash__(self):
        return hash((self.tlcorner, self.size))

    def insert(self, triangle):

        def insertAtIntersectingQuadrants(t):
            centerpoint = (self.tlcorner[0] + self.size/2, self.tlcorner[1] - self.size/2)

            if geometry.inTriangle(centerpoint, t):
                quadrants = [self.upperleft, self.upperright, self.lowerleft, self.lowerright]
            else:
                quadrants = set([self.findquadrant(t[i]) for i in range(3)])

            for q in quadrants:
                q.insert(t)

        if self.leaf:

            if self.count < self.threshold:

                self.data.append(triangle)
                self.count += 1

            else:
                childsize = self.size / 2

                self.upperleft = adaptive2Dgrid(self.tlcorner, childsize, self.threshold)
                self.upperright = adaptive2Dgrid((self.tlcorner[0] + childsize, self.tlcorner[1]), childsize, self.threshold)
                self.lowerleft = adaptive2Dgrid((self.tlcorner[0], self.tlcorner[1] - childsize), childsize, self.threshold)
                self.lowerright = adaptive2Dgrid((self.tlcorner[0] + childsize, self.tlcorner[1] - childsize), childsize, self.threshold)

                # add triangle to every quadrant containing one of the triangle's vertices
                for t in self.data + [triangle]:
                    insertAtIntersectingQuadrants(t)

                del self.data
                del self.count
                self.leaf = False

        else:
            insertAtIntersectingQuadrants(triangle)

    def find(self, point):
        leaf = self.findLeaf(point)
        result = []
        for triangle in leaf.data:
            if geometry.inTriangle(point, triangle):
                result.append(triangle)
        return result

    def findLeaf(self, point):
        q = self.findquadrant(point)
        if q.leaf:
            return q
        else:
            return q.findLeaf(point)


    def findquadrant(self, point):

        childsize = self.size / 2
        hincrement = np.array([childsize, 0])
        vincrement = np.array([0, -childsize])

        center = self.tlcorner + hincrement + vincrement

        px = point[0]
        py = point[1]
        cx = center[0]
        cy = center[1]

        if px <= cx:
            if py <= cy:
                return self.lowerleft
            else:
                return self.upperleft
        else:
            if py <= cy:
                return self.lowerright
            else:
                return self.upperright

    def plot(self, ax, color):
        a = self.tlcorner
        b = (self.tlcorner[0] + self.size, self.tlcorner[1])
        c = (self.tlcorner[0] + self.size, self.tlcorner[1] - self.size)
        d = (self.tlcorner[0], self.tlcorner[1] - self.size)

        cellsegments = [[a, b], [b, c], [c, d], [d, a]]
        lc = mc.LineCollection(cellsegments, linewidths=0.5, color=color)
        ax.add_collection(lc)

        if self.upperleft:
            self.upperleft.plot(ax, color)
        if self.upperright:
            self.upperright.plot(ax, color)
        if self.lowerleft:
            self.lowerleft.plot(ax, color)
        if self.lowerright:
            self.lowerright.plot(ax, color)
