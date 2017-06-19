import numpy as np
import sys

def inTriangle(p, t):
    a = np.array([t[0][0], t[0][1], 0])
    b = np.array([t[1][0], t[1][1], 0])
    c = np.array([t[2][0], t[2][1], 0])
    p = np.array([p[0], p[1], 0])

    dir1 = np.cross(p-a, b-a)[2] <= 0
    dir2 = np.cross(p-b, c-b)[2] <= 0
    dir3 = np.cross(p-c, a-c)[2] <= 0

    return dir1 == dir2 == dir3

def leftmostVertex(triangle):
    return triangle [ min( list(zip([0,1,2], triangle)), key = lambda p: p[1] ) [0] ]

def calcMeshHeightFor2DPoint(point2D, triangle3D):

    # Ray points - defined by "point" and any other point on the vertical line through (x,y)
    Xa = point2D[0]
    Ya = point2D[1]
    Za = 0

    Xb = point2D[0]
    Yb = point2D[1]
    Zb = 1

    # Plane points - defined by the corresponding face
    p0 = triangle3D[0]
    p1 = triangle3D[1]
    p2 = triangle3D[2]

    x0 = p0[0]
    y0 = p0[1]
    z0 = p0[2]

    x1 = p1[0]
    y1 = p1[1]
    z1 = p1[2]

    x2 = p2[0]
    y2 = p2[1]
    z2 = p2[2]

    # Linear system
    A = np.array([[Xa-Xb, x1-x0, x2-x0],[Ya-Yb, y1-y0, y2-y0],[Za-Zb, z1-z0, z2-z0]])
    b = np.array([Xa-x0, Ya-y0, Za-z0])

    try:
        tuv = np.linalg.solve(A, b)
    except:
        sys.stderr.write('linea algebra fail')
        return 0

    t = tuv[0]
    u = tuv[1]
    v = tuv[2]

    # Intersection point is t*(b-a) + u*(p1-p0) + v*(p2-p0)
    return t*(Zb-Za) + u*(z1-z0) + v*(z2-z0) # return z component
