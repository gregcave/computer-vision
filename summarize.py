#!/usr/bin/env python
"""summarize -- output some useful statistics of an image and plot its
histogram"""
#-------------------------------------------------------------------------------
# Boilerplate.
#-------------------------------------------------------------------------------
from __future__ import division
import cv2, sys, numpy

# Configuration.
MAXGREY = 64

#-------------------------------------------------------------------------------
# Routines.
#-------------------------------------------------------------------------------
def statistics (im, indent="  "):
    "Output statistical values that describe an image."
    # Calculate the statistics.
    Il = im.min ()
    Ih = im.max ()
    ave = im.mean ()
    sd  = im.std ()
    
    # Form and return the message.
    text = ""
    text += "%sMinimum: %.2f\n" % (indent, Il)
    text += "%sMaximum: %.2f\n" % (indent, Ih)
    text += "%sMean:    %.2f\n" % (indent, ave)
    text += "%sS.D.:    %.2f\n" % (indent, sd)
    return text

def histogram (im, fn, limits = None):
    "Determine the histogram of an image -- simple version."
    global MAXGREY

    if limits is None: limits = [im.min(), im.max()]
    lo, hi = limits

    # We shall fill the array hist with the histogram.
    hist = numpy.zeros (MAXGREY)
    hist2 = numpy.zeros (MAXGREY)
    red = numpy.zeros (MAXGREY)
    green = numpy.zeros (MAXGREY)
    blue = numpy.zeros (MAXGREY)

    inc = (hi - lo) / (MAXGREY - 1)
    for i in range (0, MAXGREY):
        hist2[i] = lo + i * inc

    # Get the image sizes.
    sizes = im.shape
    if len (sizes) == 2:
        # it's monochrome
        ny = sizes (0)
        nx = sizes (1)
        nc = 1
    else:
        # it has several channels
        ny, nx, nc = sizes
    
    # Work through the image, accumulating the histogram.
    for y in range (0, ny):
        for x in range (0, nx):
            for c in range (0, nc):
                if c == 0:
                    r = int ((im[y, x, c] - lo) / (hi - lo) * (MAXGREY -1) + 0.5)
                if c == 1:
                    g = int ((im[y, x, c] - lo) / (hi - lo) * (MAXGREY -1) + 0.5)
                if c == 2:
                    b = int ((im[y, x, c] - lo) / (hi - lo) * (MAXGREY -1) + 0.5)

                if r >= 0 and r < MAXGREY:
                    red[r] += 1.0
                if g >= 0 and g < MAXGREY:
                    green[g] += 1.0
                if b >= 0 and b < MAXGREY:
                    blue[b] += 1.0
                    
                #v = int ((im[y, x, c] - lo) / (hi - lo) * (MAXGREY -1) + 0.5)
                #if v >= 0 and v < MAXGREY:
                    #hist[v] += 1.0

    # Output the histogram values to a file.
    with open (fn, "w") as f:
        for i in range (0, MAXGREY):
            print >>f, i, red[i], green[i], blue[i]

    return hist2, red, green, blue

#-------------------------------------------------------------------------------
# Main program.
#-------------------------------------------------------------------------------
# We want to be invoked with some arguments on the command line.
if len (sys.argv) < 2:
    print >>sys.stderr, "Usage:", sys.argv[0], "<image>..."
    sys.exit (1)

# Process each file on the command line in turn.
for fn in sys.argv[1:]:
    im = cv2.imread (fn)

    # Output its statistics.
    print fn + ":"
    print statistics (im)

    # Calculate and output the histogram data.
    histogram (im, fn + ".dat")

#-------------------------------------------------------------------------------
# End of summarize.
#-------------------------------------------------------------------------------
