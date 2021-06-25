import cv2


# inverting the image
def get_invert(given_image):
    given_image = 255 - given_image
    return given_image


# setting a gaussian blur
def get_gaussian_blur(given_image):
    # gray = cv2.cvtColor(given_image, cv2.COLOR_BGR2GRAY)
    given_image = cv2.GaussianBlur(given_image, (3, 3), 2)
    # given_image = cv2.medianBlur(given_image, 3)  # kernel size 3
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(given_image, cv2.MORPH_CLOSE, rectKernel)
    return close


# applying a grayscale to given image
def get_grayscale(given_image):
    given_image = cv2.threshold(given_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    return given_image


# removing small unnecessary noise from the image, clearing the image
def remove_small_noise(given_image):
    cnts = cv2.findContours(given_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 10:
            cv2.drawContours(given_image, [c], -1, 0, -1)
