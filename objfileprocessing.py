class objbased_normalized_mesh:
    def __init__(self, xspan, yspan, zspan, veritces, faces):
        self.xspan = xspan
        self.yspan = yspan
        self.zspan = zspan
        self.vertices = vertices
        self.faces = faces

    def __init__(self, filename):
        vertices = []
        faces = []

        # read vertices
        objfile = open(filename)
        for line in objfile:
            if line[0:2] == 'v ':
                vertices.append(self.__parseVertex(line[2:]))

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
                faceOffsets = self.__parseFaceOffsets(line[2:])
                a = vertices[faceOffsets[0] - 1]
                b = vertices[faceOffsets[1] - 1]
                c = vertices[faceOffsets[2] - 1]
                faces.append((a, b, c))

        self.vertices = vertices
        self.faces = faces
        self.xspan = xmax - xmin
        self.yspan = ymax - ymin
        self.zspan = zmax - zmin

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
