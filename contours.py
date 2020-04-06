#!/usr/bin/env python
"contours -- demo of OpenCV's contour-processing capabilities"
from __future__ import division
import sys, cv2

# Handle the command line.
if len (sys.argv) < 3:
    print >>sys.stderr, "Usage:", sys.argv[0], "<image> <threshold>"
    sys.exit (1)
img = cv2.imread (sys.argv[1])
t = int (sys.argv[2])

# Count the number of dots on the dice faces.We do this by iterating over
# hierarchy[0], first to find the indices of the dice contours, then again
# to find the dot contours.
dice = []
# list of dice contours
dots = []



# Produce a binary image.
gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur (gray, (5, 5), 0)
(t, binary) = cv2.threshold (blur, t, 255, cv2.THRESH_BINARY)
#binary = cv2.adaptiveThreshold (blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 11, 2)
#t, binary = cv2.threshold (blur, 0, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Find contours.
#(_, contours, _) = cv2.findContours (binary, cv2.RETR_EXTERNAL, 
#    cv2.CHAIN_APPROX_SIMPLE)

# Find internal contours too.
#(_, contours, hierarchy) = cv2.findContours(binary, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
(junk, contours, hierarchy) = cv2.findContours(binary,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Find the dice contours.
for (i, c) in enumerate (hierarchy[0]):
    if c[3] == -1:
        dice.append (i)

# Now find the dot contours, and output how many we find.
for (i, c) in enumerate (hierarchy[0]):
    if c[3] in dice:
        dots.append (i)
print "Total number of dots:", len (dots)


# Print a table of the contours and their sizes.
print "Found %d objects." % len(contours)
for (i, c) in enumerate(contours):
    print "\tSize of contour %d: %d" % (i, len(c))
    
    # Draw the contours over the original image and display the result.
    if len(c) > 250:
        cv2.drawContours (img, contours, i, (0, 0, 255), 5)
    if (len(c) < 250 and len (c) > 30):
        cv2.drawContours (img, contours, i, (0, 255, 0), 5)
    if len (c) < 30:
        cv2.drawContours (img, contours, i, (255, 0, 0), 5)
    
cv2.namedWindow (sys.argv[0], cv2.WINDOW_NORMAL)
ny, nx, nc = img.shape
cv2.resizeWindow (sys.argv[0], nx//2, ny//2)
cv2.imshow (sys.argv[0], img)
cv2.waitKey (0)
