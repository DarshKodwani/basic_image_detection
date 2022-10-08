import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw

filename = 'src/ring.png'

# Loads an image
src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
gray = cv.medianBlur(gray, 5)
rows = gray.shape[0]
print('Finding circles')
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 3000, param1=100, param2=30, minRadius=900, maxRadius=1100)

print('Finding circle outlines')
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        print(f'Circle {i}')
        center = (i[0], i[1])
        # circle center
        cv.circle(src, center, 1, (0, 100, 100), 3)
        # circle outline
        radius = i[2]
        cv.circle(src, center, radius, (255, 0, 255), 3)

cv.circle(src, center, 1, (0, 100, 100), 3)
cv.circle(src, center, np.int32(np.round(radius*0.7)), (255, 0, 255), 3)

xright = center[0] + radius
xleft = center[0] - radius
ytop = center[1] + radius
ydown = center[1] - radius 

img = Image.fromarray(src)
img_cropped = img.crop((xleft, ydown, xright, ytop))

# create grayscale image with white circle (255) on black background (0)
mask = Image.new('L', img_cropped.size)
mask_draw = ImageDraw.Draw(mask)
width, height = img_cropped.size
mask_draw.ellipse((0, 0, width, height), fill=255)
#mask.show()

# add mask as alpha channel
img_cropped.putalpha(mask)

# save as png which keeps alpha channel 
img_cropped.save('cropped_ring.png')

img_cropped.show()