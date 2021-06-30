from image_to_plate import *


cam = cv2.VideoCapture("../test_data/video1.mp4")


# change camera settings
# focus = 0
# cam.set(cv2.CAP_PROP_SATURATION, -15)
# cam.set(cv2.CAP_PROP_GAIN, 12)
# cam.set(cv2.CAP_PROP_EXPOSURE, 1 / 50)  # set shutter speed longer better -> no blur but for cars less then 10km/h
# cam.set(28, focus)  # min: 0, max: 255, increment:5,
# the key 28 is for setting focus

while True:
    ret, img = cam.read()

    if cv2.waitKey(10) == ord('q'):
        break
    # make sure to disable __init__ at image_to_plate.py
    get_image_to_plate(img, True)

cv2.destroyAllWindows()


'''  Adjusting camera properties
       key value
cam.set(3 , 640  ) # width       
cam.set(4 , 480  ) # height       
cam.set(10, 120  ) # brightness     min: 0   , max: 255 , increment:1 
cam.set(11, 50   ) # contrast       min: 0   , max: 255 , increment:1     
cam.set(12, 70   ) # saturation     min: 0   , max: 255 , increment:1
cam.set(13, 13   ) # hue         
cam.set(14, 50   ) # gain           min: 0   , max: 127 , increment:1
cam.set(15, -3   ) # exposure       min: -7  , max: -1  , increment:1
cam.set(17, 5000 ) # white_balance  min: 4000, max: 7000, increment:1
cam.set(28, 0    ) # focus          min: 0   , max: 255 , increment:5
'''

