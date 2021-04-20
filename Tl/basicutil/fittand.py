import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
import scipy.interpolate
import scipy.signal
import numpy as np
import sys
import os
import re

if len(sys.argv) != 2:
    print "error you need to specify at least a file"
    exit(1)

if not (os.path.isfile(sys.argv[1])):
    print("File " + sys.argv[i] + " does not exist ")
    exit(1)

fp = open(sys.argv[1])

xl = []
yl = []

for line in fp:
    p = re.compile(r'\s+')
    line = p.sub(' ', line)
    line = line.lstrip()
    line = line.rstrip()
    
    sline = line.split(" ")
    if len(sline) != 2:
      print "error in parsing file ", sys.argv[1]
      exit(1)

    xl.append(np.float64(sline[0])*0.529177)
    yl.append(np.float64(sline[1])*27.2114)

fp.close()

x = np.array(xl)
y = np.array(yl)

coefs = poly.polyfit(x, y, 4)

x_new = np.linspace(x[0], x[-1], num=len(x)*10)
y_new = poly.polyval(x_new, coefs)

ymin = np.min(y_new)
i, = np.where(y_new == ymin)
xmin = x_new[i[0]]

print "Xmin: ", xmin

plt.plot(xmin, ymin, '*')
plt.plot(x, y, 'ro')
plt.plot(x_new, y_new, 'b--')
plt.show()

# This class returns a function whose call method uses 
# interpolation to find the value of new points.
#f = scipy.interpolate.interp1d(x,y)

#xmin = np.min(x)
#xmax = np.max(x)
# using 1000 samples
#xx = np.linspace(xmin, xmax, 1000)

# compute the function on this finer interval
#yy = f(xx)

# make a gaussian window
#window = scipy.signal.gaussian(200, 60)

# convolve the arrays
#smoothed = scipy.signal.convolve(yy, window/window.sum(), mode='same')

# get the maximum
#ymin = np.min(yy)
#i, = np.where(yy == ymin)
#xmin2 = xx[np.argmin(smoothed)]
#xmin = xx[i[0]]

#print "Xmin: ", xmin

#plt.plot(x, y, 'ro')
#plt.plot(xmin, ymin, '*')
#plt.plot(xmin2, ymin, '*')
#plt.plot(xx, yy, 'b--')
#plt.show()
