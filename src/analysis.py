import cv2 as cv
import os
import numpy as np
from PIL import Image, ImageDraw

def find_circles(image):
    print('Finding circles')
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 3000, param1=100, param2=30, minRadius=900, maxRadius=1100)
    return circles


def crop_image_to_circle(image, circles, inner_radius_fraction=0.7):
    print('Finding circle outlines')
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            print(f'Circle {i}')
            center = (i[0], i[1])
            # circle center
            cv.circle(image, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(image, center, radius, (255, 0, 255), 3)

    cv.circle(image, center, 1, (0, 100, 100), 3)
    cv.circle(image, center, np.int32(np.round(radius*inner_radius_fraction)), (255, 0, 255), 3)
    cv.imwrite(os.path.join(os.environ['REPO_ROOT'], 'src/detected_circles_ring.png'), image)

    xright = center[0] + radius
    xleft = center[0] - radius
    ytop = center[1] + radius
    ydown = center[1] - radius

    img = Image.fromarray(image)
    img_cropped = img.crop((xleft, ydown, xright, ytop))

    # create grayscale image with white circle (255) on black background (0)
    mask = Image.new('L', img_cropped.size)
    mask_draw = ImageDraw.Draw(mask)
    width, height = img_cropped.size
    mask_draw.ellipse((0, 0, width, height), fill=255)

    # add mask as alpha channel
    img_cropped.putalpha(mask)

    return img_cropped

def get_histograms(img_cropped):
    red_hist = img_cropped.split()[0].histogram()
    blue_hist = img_cropped.split()[1].histogram()
    green_hist = img_cropped.split()[2].histogram()
    hist_dict = {'red': red_hist, 'blue': blue_hist, 'green': green_hist}
    return hist_dict

def detect_ring(hist_dict, detection_threshold_for_median=7000):
    medians = []
    for i in ['red', 'blue', 'green']:
        median = np.median(hist_dict[i])
        medians.append(median)
    if np.mean(medians) < detection_threshold_for_median:
        print(' ---------------------------------')
        print('|              No Ring!           |')
        print(' ---------------------------------')
        return ['No ring found']
    else:
        print(' ---------------------------------')
        print('|            Ring found!          |')
        print(' ---------------------------------')
        return ["Ring found"]

def run_ring_detection(image):
    circles = find_circles(image)
    cropped_image = crop_image_to_circle(image, circles)
    hist_dict = get_histograms(cropped_image)
    return detect_ring(hist_dict)

if __name__ == "__main__":
    filename = 'src/ring.png'
    image = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)
    run_ring_detection(image)