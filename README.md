# Description
A script to generate surface elevation maps for 3D triangular meshes with a large number of faces. The program samples the mesh height values (z axis) at a user-specified resolution and outputs the corresponding heightmap. It relies on an adaptive quadtree structure for efficient lookup of mesh faces and supports multi-threaded processing. Threaded execution is supported.

# Usage
The script takes the input mesh file in .obj format as a command line argument. After processing the input file, you will be prompted to specify the heightmap resolution, number of threads to be used, output file address and a matplotlib colormap (default is 'viridis').

# Example
On the right, an orthomosaic of a landscape 3D mesh. On the left, a 1600x1600 heightmap for that mesh generated with this script. Missing face information in the mesh is set to a height of zero by default, so "holes" can be observed in the resulting map if they exist in the input mesh.

![alt text](example/heightmapVsOrthomosaic.png)
