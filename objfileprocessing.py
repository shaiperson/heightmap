from adaptive2Dgrid import adaptive2Dgrid
import geometry
from sys import stderr

ADAPTIVE_2D_GRID_THRESHOLD = 100

def isValidTriangle(t):
    return t[0] != t[1] and t[1] != t[2] and t[0] != t[2]

class objbased_normalized_mesh:
    def __init__(self, xspan, yspan, zspan, veritces, faces):
        self.xspan = xspan
        self.yspan = yspan
        self.zspan = zspan
        self.vertices = vertices
        self.faces = faces

    def __init__(self, filename):
        vertices = []

        # read vertices while calculating x, y and z ranges
        xmin = ymin = zmin = float('inf')
        xmax = ymax = zmax = -float('inf')

        with open(filename) as objfile:
            for line in objfile:
                if line[0:2] == 'v ':
                    # parse and save vertex
                    v = self.__parseVertex(line[2:])
                    vertices.append(v)

                    # update mins and maxs
                    (x, y, z) = v
                    if x < xmin:
                        xmin = x
                    elif x > xmax:
                        xmax = x
                    if y < ymin:
                        ymin = y
                    elif y > ymax:
                        ymax = y
                    if z < zmin:
                        zmin = z
                    elif z > zmax:
                        zmax = z

        self.xspan = xmax - xmin
        self.yspan = ymax - ymin
        self.zspan = zmax - zmin

        # normalize vertices (translate positive octate)
        vertices = [(v[0] - xmin, v[1] - ymin, (v[2] - zmin)/self.zspan) for v in vertices]
        self.vertices = vertices

        # read faces into quadtree-based 2D adaptive grid using normalized vertices
        self.faces = adaptive2Dgrid( (0, self.yspan), max(self.xspan, self.yspan),  ADAPTIVE_2D_GRID_THRESHOLD)
        with open(filename) as objfile:
            for line in objfile:
                if line[0:2] == 'f ':
                    faceOffsets = self.__parseFaceOffsets(line[2:])
                    a = vertices[faceOffsets[0] - 1]
                    b = vertices[faceOffsets[1] - 1]
                    c = vertices[faceOffsets[2] - 1]
                    if isValidTriangle((a, b, c)):
                        self.faces.insert((a, b, c))
                    else:
                        print('Non-triangle in .obj: ', (a, b, c), file=stderr)

    def faces_for_2D_point(self, point):
        #return self.faces.find(point)
        qtree_node = self.faces
        while not qtree_node.leaf:
            qtree_node = qtree_node.findquadrant(point)
        return [ triangle for triangle in qtree_node.data if geometry.inTriangle(point, triangle) ]

    def write(self, filename):
        f = open(filename, 'w')
        print(self.xspan, file=f)
        print(self.yspan, file=f)
        print(self.zspan, file=f)
        print(self.vertices, file=f)
        print(self.faces, file=f)
        f.close()

    def __parseVertex(self, str):
        s = str.split(' ')
        return (float(s[0]), float(s[1]), float(s[2]))

    def __parseFaceOffsets(self, str):
        s = str.split(' ')
        return (int((s[0].split('/'))[0]), int((s[1].split('/'))[0]), int((s[2].split('/'))[0]))
