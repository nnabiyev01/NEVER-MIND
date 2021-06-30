import cv2
import imutils
import numpy as np
from image_filters import apply_filter


# initialising and preparing image and gray_image
def prepare_image(image_path, is_path):
    if is_path:
        local_img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    else:
        local_img = image_path
    local_img = cv2.resize(local_img, (620, 480))

    local_gray = cv2.cvtColor(local_img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
    # local_gray = cv2.bilateralFilter(local_gray, 11, 17, 17)  # Blur to reduce noise
    # local_gray = cv2.equalizeHist(local_gray)  # histogram equalization

    kernel = np.ones((1, 1), np.uint8)
    local_gray = cv2.dilate(local_gray, kernel, iterations=1)
    local_gray = cv2.erode(local_gray, kernel, iterations=1)
    return local_img, local_gray


# edge detection and marking using image and gray_image
def edge_detection(given_image, given_gray_image):
    # very important for square detection
    blurred = cv2.GaussianBlur(given_gray_image, (3, 3), 0)
    edged = cv2.Canny(blurred, 120, 255, 1)  # Perform Edge detection

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    local_screen_cnt = None

    for c in cnts:
        rect = cv2.minAreaRect(c)  # Find the minimum enclosing rectangle center point, width and height, angle
        if rect[1][1] > rect[1][0]:
            k = rect[1][1] / rect[1][0]
        else:
            k = rect[1][0] / rect[1][1]
        if (k > 1.2) & (k < 6):  # Judge the outline of the license plate

            a = cv2.boxPoints(rect)  # Get the four points of the bounding rectangle
            box = np.int0(a)
            local_screen_cnt = box
            break
    if local_screen_cnt is None:
        return None
    else:
        cv2.drawContours(given_image, [local_screen_cnt], -1, (0, 255, 0), 3)
    return local_screen_cnt


# getting mask based on detected edge
def get_mask(given_image, given_gray_image, given_screen_cnt):
    # Masking the part other than the number plate
    local_mask = np.zeros(given_gray_image.shape, np.uint8)
    cv2.drawContours(local_mask, [given_screen_cnt], 0, 255, -1, )
    cv2.bitwise_and(given_image, given_image, mask=local_mask)
    return local_mask


# cropping the image based on given mask
def get_crop(given_gray_image, given_mask):
    (x, y) = np.where(given_mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    return given_gray_image[topx:bottomx + 1, topy:bottomy + 1]


# returns extracted crop from given image
def get_image_to_crop(image_path, show_extraction_process):
    cropped = None
    image, gray_image = prepare_image(image_path, False)

    screen_cnt = edge_detection(image, gray_image)
    if screen_cnt is not None:
        mask = get_mask(image, gray_image, screen_cnt)
        cropped = get_crop(gray_image, mask)
        cropped = apply_filter(cropped)

        if show_extraction_process:
            # displaying image with outline of the cropped part
            cv2.imshow('Image', image)  # optional

    return cropped
