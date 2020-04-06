#!/usr/bin/env python
"Demonstrate content-based image retrieval using histograms"
import sys, math, cv2, numpy

# The number of bins in a histogram.
NBINS = 64

#------------------------------------------------------------------------------
def compare (h1, h2):
    "Work out the correlation between two histograms"
    sumx = sumy = sumxx = sumyy = sumxy = 0.0
    n = len (h1)
    for i in range (0, n):
        v1 = float (h1[i])
        v2 = float (h2[i])
        sumx += v1
        sumy += v2
        sumxx += v1 * v1
        sumxy += v1 * v2
        sumyy += v2 * v2
    v1 = sumxy - sumx * sumy / n
    v2 = math.sqrt((sumxx-sumx*sumx/n) * (sumyy-sumy*sumy/n))
    return abs (v1 / v2)

def hist (im):
    "Return the grey-level histogram of an image."
    global NBINS

    # Determine the data range.
    lo = im.min ()
    hi = im.max ()

    # Compute the histogram and return it.
    h, bins = numpy.histogram (im.ravel(), NBINS, [lo, hi])
    return h

#------------------------------------------------------------------------------
# Say hello and initialize things.
if len(sys.argv) < 3:
    print >>sys.stderr, 'Usage:', sys.argv[0], '<probe> <test-images>'
    sys.exit (1)
probe_file = sys.argv[1]
v_best = 0
f_best = '?'

# Read in the probe image and find its histogram.
im = cv2.imread (probe_file)
probe = hist (im)

# We now enter the main loop.  The basic idea is to load an image, find its
# histogram, then compare that with the histogram of the probe image.  We are
# careful to skip the case when the test image is the same as the probe.
for file in sys.argv[2:]:
    if file != probe_file:
        im = cv2.imread (file)
        h = hist (im)
        v = compare (probe, h)
        if v > v_best:
            v_best = v
            f_best = file

# We've finished our work, so say which of the test set best matches the
# probe and exit.
print f_best
