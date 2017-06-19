def readAndNormalizeMesh(filename):
    vertices = []
    faces = []

    # read vertices
    objfile = open(filename)
    for line in objfile:
        if line[0:2] == 'v ':
            vertices.append(parseVertex(line[2:]))

    # calculate ranges -- TODO: compute while reading vertex info, not afterwards
    xmin = min([v[0] for v in vertices])
    xmax = max([v[0] for v in vertices])

    ymin = min([v[1] for v in vertices])
    ymax = max([v[1] for v in vertices])

    zmin = min([v[2] for v in vertices])
    zmax = max([v[2] for v in vertices])

    # normalize vertices (translate positive octate)
    vertices = [(v[0] - xmin, v[1] - ymin, v[2] - zmin) for v in vertices]

    # read faces using normalized vertices
    objfile = open(filename)
    for line in objfile:
        if line[0:2] == 'f ':
            faceOffsets = parseFaceOffsets(line[2:])
            a = vertices[faceOffsets[0]-1]
            b = vertices[faceOffsets[1]-1]
            c = vertices[faceOffsets[2]-1]
            faces.append((a, b, c))

    return vertices, faces, xmax-xmin, ymax-ymin, zmax-zmin

def parseVertex(str):
    s = str.split(' ')
    return (float(s[0]), float(s[1]), float(s[2]))

def parseFaceOffsets(str):
    s = str.split(' ')
    return (int((s[0].split('/'))[0]), int((s[1].split('/'))[0]), int((s[2].split('/'))[0]))
