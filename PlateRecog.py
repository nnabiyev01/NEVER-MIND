import cv2
import imutils
import numpy as np
import pytesseract
from text_plate_extractor import get_plate
import image_filters


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
    # very imporant for square detection
    blurred = cv2.GaussianBlur(given_gray_image, (3, 3), 0)
    edged = cv2.Canny(blurred, 120, 255, 1)  # Perform Edge detection
    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    local_screen_cnt = None

    """CHECKING ALL THE CONTOURS
    
    # print("Number of Contours found : " + str(len(cnts)))
    # for c in cnts:
    #     x, y, w,  h = cv2.boundingRect(c)
    #     print(x, y, w, h)
    #
    #     peri = cv2.arcLength(c, True)
    #     approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    #     local_screen_cnt = approx
    #     cv2.drawContours(given_image, [local_screen_cnt], -1, (0, 255, 0), 3)
    # return
    
     """

    # loop over our contours
    for c in cnts:
        # approximate the contour

        x, y, w, h = cv2.boundingRect(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) and 1.2 < w / h < 6:
            print(x, y, w, h)
            local_screen_cnt = approx
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
    # print(pytesseract.get_tesseract_version())
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


def find_the_correct_text_option(sets):
    false_extract = []
    plate_num, image_to_text = "00"
    for k, v in sets.items():
        if sets[k]:
            image_to_text = k
            plate_num = sets[k]
            return image_to_text, plate_num, false_extract

        else:
            false_extract.append(k)
            plate_num = v
    return image_to_text, plate_num, false_extract


def execute():
    """ Executed Tasks """
    # preparing, cropping, filtering the image for read
    image, gray_image = prepare_image("test_data/image1.jpg", True)
    screen_cnt = edge_detection(image, gray_image)
    if screen_cnt is not None:
        mask = get_mask(image, gray_image, screen_cnt)
        cropped = get_crop(gray_image, mask)
        cropped = apply_filter(cropped)
        # reading the image
        dict = read_plate_number(cropped)
        # getting the correct text option
        extraction, plate_text, wrong_extractions = find_the_correct_text_option(dict)
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


execute()
