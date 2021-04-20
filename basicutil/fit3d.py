import sys
import itertools
import numpy 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource

#######################################################################

def poly_matrix (x, y, order=2):

    ncols = (order + 1)**2
    G = numpy.zeros((x.size, ncols))
    ij = itertools.product(range(order+1), range(order+1))
    for k, (i, j) in enumerate(ij):
        G[:, k] = x**i * y**j
    return G

#######################################################################

def file_len(fname):
    
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    
    return i + 1

#######################################################################

filename = ""

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print "usage: ", sys.argv[0], " filename "
    exit(1)

numofln = file_len(filename)

points = numpy.zeros((numofln, 3), numpy.float64 )

fp = open(filename)

i = 0
for l in fp:
    line = ' '.join(l.split())
    sline = line.split()
    if len(sline) == 3:
        points[i, 0] = numpy.float64(sline[0])
        points[i, 1] = numpy.float64(sline[1])
        points[i, 2] = numpy.float64(sline[2])
        i = i + 1

ordr = 2  # order of polynomial
x, y, z = points.T

centerx = numpy.min(x)
centery = numpy.min(y)

#x, y = x - centerx, y - centery  # this improves accuracy

# make Matrix:
G = poly_matrix(x, y, ordr)
# Solve for numpy.dot(G, m) = z:
m = numpy.linalg.lstsq(G, z)[0]

# Evaluate it on a grid...
nx, ny = 50, 50
xx, yy = numpy.meshgrid(numpy.linspace(x.min(), x.max(), nx),
                     numpy.linspace(y.min(), y.max(), ny))
GG = poly_matrix(xx.ravel(), yy.ravel(), ordr)
zz = numpy.reshape(numpy.dot(GG, m), xx.shape)


fg, ax = plt.subplots(subplot_kw=dict(projection='3d'))
ls = LightSource(270, 45)
rgb = ls.shade(zz, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(xx, yy, zz, rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=False)
ax.plot3D(x, y, z, "o")

zmin = numpy.min(zz)
itemindex = numpy.where(zz==zmin)

#print itemindex[0][0], itemindex[1][0]

#[(index, row.index(val)) for index, row in enumerate(zz) if zmin in row]
#print index
xx = numpy.linspace(x.min(), x.max(), nx)
yy = numpy.linspace(y.min(), y.max(), ny)

xmin = xx[itemindex[1][0]]
ymin = yy[itemindex[0][0]]
print xmin, ymin, zmin
print xmin + centerx, ymin + centery

fg.canvas.draw()
plt.show()
