import cv2
import imutils
import numpy as np
import pytesseract
import database
from text_plate_extractor import get_plate
from PIL import Image


img = cv2.imread('/home/nabi/Pictures/5.jpg', cv2.IMREAD_COLOR)

img = cv2.resize(img, (620, 480))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
# gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
kernel = np.ones((1, 1), np.uint8)
gray = cv2.dilate(gray, kernel, iterations=1)
gray = cv2.erode(gray, kernel, iterations=1)

edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
screenCnt = None

# loop over our contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)

    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print("No contour detected")
else:
    detected = 1

if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

    # Masking the part other than the number plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
    new_image = cv2.bitwise_and(img, img, mask = mask)


    # Now crop
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]


    # Read the number plate
    character_whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- "
    text = pytesseract.image_to_string(Cropped, config="--psm 11"
                                       "_char_whitelist=" + character_whitelist)
    print(text)
    text = get_plate(text)
    print(text)

    if text:
        ''' Database  '''
        # Call the database and add the plate numbers
        database = database.Database(text)
        flag = database.connect()

        # open and close the gates
        if flag:
            print(" Entered ")
            # open the entrance gate
        elif not flag:
            print(" Exited ")
            # open the exit gate

    cv2.imshow('Cropped', Cropped)

# text = pytesseract.image_to_string(Cropped, config='-l eng --oem 3 --psm 11')

#check all details
# test = pytesseract.image_to_data(Cropped, config = '')

# print(test)

cv2.imshow('image', img)



cv2.waitKey(0)
cv2.destroyAllWindows()
