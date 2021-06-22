import cv2
import imutils
import numpy as np
import pytesseract
from text_plate_extractor import get_plate
import image_filters


# initialising and preparing image and gray_image
def prepare_image(image_path):
    local_img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    local_img = cv2.resize(local_img, (620, 480))

    local_gray = cv2.cvtColor(local_img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
    # local_gray = cv2.bilateralFilter(local_gray, 11, 17, 17)  # Blur to reduce noise
    kernel = np.ones((1, 1), np.uint8)
    local_gray = cv2.dilate(local_gray, kernel, iterations=1)
    local_gray = cv2.erode(local_gray, kernel, iterations=1)
    return local_img, local_gray


# edge detection and marking using image and gray_image
def edge_detection(given_image, given_gray_image):
    edged = cv2.Canny(given_gray_image, 30, 200)  # Perform Edge detection
    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    local_screen_cnt = None

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            local_screen_cnt = approx
            break

    if local_screen_cnt is None:
        print("No contour detected")
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


# applying filter for the cropped image
# enhances tesseracts readability
def apply_filter(given_image):
    given_image = image_filters.get_grayscale(given_image)
    image_filters.remove_small_noise(given_image)
    given_image = image_filters.get_invert(given_image)
    given_image = image_filters.get_gaussian_blur(given_image)
    return given_image


# reading the plate number based on crop
def read_plate_number(given_crop):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    # string_whitelist = "C:/Program Files/Tesseract-OCR/tessdata/eng.user-patterns"
    character_whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- "

    # text output option 1 -> use --psm11
    text_opt1 = pytesseract.image_to_string(given_crop, lang='eng',
                                            config="--psm 11 _char_whitelist=" + character_whitelist)
    # + " --user-patterns " + string_whitelist))

    # text output option 2
    text_opt2 = pytesseract.image_to_string(given_crop, lang='eng', config="_char_whitelist=" + character_whitelist)

    # check the statistics for each option
    print(pytesseract.image_to_data(given_crop, lang='eng', config="--psm 11", output_type='data.frame'))
    print(pytesseract.image_to_data(given_crop, lang='eng', output_type='data.frame'))

    dict_of_options = {text_opt1: get_plate(text_opt1), text_opt2: get_plate(text_opt2)}

    return dict_of_options


""" Executed Tasks """
# preparing, cropping, filtering the image for read
image, gray_image = prepare_image("/home/nabi/Pictures/01.jpg")
screen_cnt = edge_detection(image, gray_image)
if screen_cnt is not None:
    mask = get_mask(image, gray_image, screen_cnt)
    cropped = get_crop(gray_image, mask)
    cropped = apply_filter(cropped)
    # reading the image
    dict = read_plate_number(cropped)

    # output
    wrong_extractions = []
    plate_text, extraction = "00"
    for k, v in dict.items():
        if dict[k]:
            extraction = k
            plate_text = dict[k]
            break
        else:
            wrong_extractions.append(k)
            plate_text = v

    if plate_text:
        print("---Extracted Text---\n" + extraction)
        print("---Plate Text---\n" + plate_text)
    else:
        print("---Extracted Text---\n" + '  1st<-->2nd  '.join(str(x) for x in wrong_extractions))
        print("---Plate Text---\n" + plate_text)

    # cropped image display
    cv2.imshow('Cropped', cropped)

# image display
cv2.imshow('Image', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
