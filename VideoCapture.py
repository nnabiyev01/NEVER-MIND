'''version 1 __main2__'''

import cv2
import pytesseract
import numpy as np
from PIL import Image
import imutils
from text_plate_extractor import get_plate
import time
import database

cam = cv2.VideoCapture("rtsp://admin:admin123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0")

# cam = cv2.VideoCapture(0)
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"  # your path may be different
while cam.isOpened():

    ret, img = cam.read()

    if cv2.waitKey(10) == ord('q'):
        break

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

    if detected == 1:
        # Masking the part other than the number plate
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
        new_image = cv2.bitwise_and(img, img, mask=mask)

        # Now crop
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

        # Read the number plate

        text = pytesseract.image_to_string(Cropped, config='--psm 11')
        # text = pytesseract.image_to_string(Cropped, config='-l eng --oem 3 --psm 11')
        plate_text = get_plate(text).replace("-", " ")
        if plate_text:
            time.sleep(15)  # maybe changed because we don't know the exact time the barrier opens and closes
            database = database.Database(plate_text)
            flag = database.connect()
            # open and close the gates
            if flag:
                # open the entrance gate
                print(" Entered ")

            elif not flag:
                # open the exit gate
                print(" Exited ")

        print(text)
        # print(test)
        cv2.imshow('Cropped', Cropped)

    cv2.imshow('image', img)

cv2.destroyAllWindows()









# end

''' REST SAMPLES ARE FOR MULTI THREADING '''

import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError

#
# class Cam():
#
#     def __init__(self, url):
#
#         # Threading for multiple cameras
#         print("bun")
#         self.stream = requests.get(url, stream=True)
#         print("bun")
#         self.thread_cancelled = False
#         self.thread = Thread(target=self.run)
#         print("camera initialised")
#
#     def start(self):
#
#         self.thread.start()
#         print("camera stream started")
#
#     def run(self):
#         bytes = ''
#         while not self.thread_cancelled:
#             try:
#                 bytes += self.stream.raw.read(1024)
#                 a = bytes.find('\xff\xd8')
#                 b = bytes.find('\xff\xd9')
#                 if a != -1 and b != -1:
#                     jpg = bytes[a:b + 2]
#                     bytes = bytes[b + 2:]
#                     img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#                     cv2.imshow('cam', img)
#
#                     #insert the plate recognition code  or call it and then that code sends the data to database
#                     if cv2.waitKey(1) == 27:
#                         exit(0)
#             except ThreadError:
#                 print("DDDD")
#                 self.thread_cancelled = True
#
#     def is_running(self):
#         return self.thread.isAlive()
#
#     def shut_down(self):
#         self.thread_cancelled = True
#         # block while waiting for thread to terminate
#         while self.thread.isAlive():
#             time.sleep(1)
#         return True
#
#
#
# url = 'http://192.168.2.1/?action=stream' #or 'rtsp://username:password@192.168.1.64/1'
# cam = Cam(url)
# print(cam)
# cam.start()


'''3 rd version ( __main__) #threading with multi camera examples but with an unnecessary GUI  '''

# from PyQt4 import QtCore, QtGui
# import qdarkstyle
# from threading import Thread
# from collections import deque
# from datetime import datetime
# import time
# import sys
# import cv2
# import imutils
#
# class CameraWidget(QtGui.QWidget):
#     """Independent camera feed
#     Uses threading to grab IP camera frames in the background
#
#     @param width - Width of the video frame
#     @param height - Height of the video frame
#     @param stream_link - IP/RTSP/Webcam link
#     @param aspect_ratio - Whether to maintain frame aspect ratio or force into fraame
#     """
#
#     def __init__(self, width, height, stream_link=0, aspect_ratio=False, parent=None, deque_size=1):
#         super(CameraWidget, self).__init__(parent)
#
#         # Initialize deque used to store frames read from the stream
#         self.deque = deque(maxlen=deque_size)
#
#         # Slight offset is needed since PyQt layouts have a built in padding
#         # So add offset to counter the padding
#         self.offset = 16
#         self.screen_width = width - self.offset
#         self.screen_height = height - self.offset
#         self.maintain_aspect_ratio = aspect_ratio
#
#         self.camera_stream_link = stream_link
#
#         # Flag to check if camera is valid/working
#         self.online = False
#         self.capture = None
#         self.video_frame = QtGui.QLabel()
#
#         self.load_network_stream()
#
#         # Start background frame grabbing
#         self.get_frame_thread = Thread(target=self.get_frame, args=())
#         self.get_frame_thread.daemon = True
#         self.get_frame_thread.start()
#
#         # Periodically set video frame to display
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.set_frame)
#         self.timer.start(.5)
#
#         print('Started camera: {}'.format(self.camera_stream_link))
#
#     def load_network_stream(self):
#         """Verifies stream link and open new stream if valid"""
#
#         def load_network_stream_thread():
#             if self.verify_network_stream(self.camera_stream_link):
#                 self.capture = cv2.VideoCapture(self.camera_stream_link)
#                 self.online = True
#         self.load_stream_thread = Thread(target=load_network_stream_thread, args=())
#         self.load_stream_thread.daemon = True
#         self.load_stream_thread.start()
#
#     def verify_network_stream(self, link):
#         """Attempts to receive a frame from given link"""
#
#         cap = cv2.VideoCapture(link)
#         if not cap.isOpened():
#             return False
#         cap.release()
#         return True
#
#     def get_frame(self):
#         """Reads frame, resizes, and converts image to pixmap"""
#
#         while True:
#             try:
#                 if self.capture.isOpened() and self.online:
#                     # Read next frame from stream and insert into deque
#                     status, frame = self.capture.read()
#                     if status:
#                         self.deque.append(frame)
#                     else:
#                         self.capture.release()
#                         self.online = False
#                 else:
#                     # Attempt to reconnect
#                     print('attempting to reconnect', self.camera_stream_link)
#                     self.load_network_stream()
#                     self.spin(2)
#                 self.spin(.001)
#             except AttributeError:
#                 pass
#
#     def spin(self, seconds):
#         """Pause for set amount of seconds, replaces time.sleep so program doesnt stall"""
#
#         time_end = time.time() + seconds
#         while time.time() < time_end:
#             QtGui.QApplication.processEvents()
#
#     def set_frame(self):
#         """Sets pixmap image to video frame"""
#
#         if not self.online:
#             self.spin(1)
#             return
#
#         if self.deque and self.online:
#             # Grab latest frame
#             frame = self.deque[-1]
#
#             # Keep frame aspect ratio
#             if self.maintain_aspect_ratio:
#                 self.frame = imutils.resize(frame, width=self.screen_width)
#             # Force resize
#             else:
#                 self.frame = cv2.resize(frame, (self.screen_width, self.screen_height))
#
#             # Add timestamp to cameras
#             cv2.rectangle(self.frame, (self.screen_width-190,0), (self.screen_width,50), color=(0,0,0), thickness=-1)
#             cv2.putText(self.frame, datetime.now().strftime('%H:%M:%S'), (self.screen_width-185,37), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), lineType=cv2.LINE_AA)
#
#             # Convert to pixmap and set to video frame
#             self.img = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
#             self.pix = QtGui.QPixmap.fromImage(self.img)
#             self.video_frame.setPixmap(self.pix)
#
#     def get_video_frame(self):
#         return self.video_frame
#
# def exit_application():
#     """Exit program event handler"""
#
#     sys.exit(1)
#
# if __name__ == '__main__':
#
#     # Create main application window
#     app = QtGui.QApplication([])
#     app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())
#     app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
#     mw = QtGui.QMainWindow()
#     mw.setWindowTitle('Camera GUI')
#     mw.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#
#     cw = QtGui.QWidget()
#     ml = QtGui.QGridLayout()
#     cw.setLayout(ml)
#     mw.setCentralWidget(cw)
#     mw.showMaximized()
#
#     # Dynamically determine screen width/height
#     screen_width = QtGui.QApplication.desktop().screenGeometry().width()
#     screen_height = QtGui.QApplication.desktop().screenGeometry().height()
#
#     # Create Camera Widgets
#     username = 'Your camera username!'
#     password = 'Your camera password!'
#
#     # Stream links
#     camera0 = 'rtsp://{}:{}@192.168.1.43:554/cam/realmonitor?channel=1&subtype=0'.format(username, password)
#     camera1 = 'rtsp://{}:{}@192.168.1.45/axis-media/media.amp'.format(username, password)
#     camera2 = 'rtsp://{}:{}@192.168.1.47:554/cam/realmonitor?channel=1&subtype=0'.format(username, password)
#     camera3 = 'rtsp://{}:{}@192.168.1.40:554/cam/realmonitor?channel=1&subtype=0'.format(username, password)
#     camera4 = 'rtsp://{}:{}@192.168.1.44:554/cam/realmonitor?channel=1&subtype=0'.format(username, password)
#     camera5 = 'rtsp://{}:{}@192.168.1.42:554/cam/realmonitor?channel=1&subtype=0'.format(username, password)
#     camera6 = 'rtsp://{}:{}@192.168.1.46:554/cam/realmonitor?channel=1&subtype=0'.format(username, password)
#     camera7 = 'rtsp://{}:{}@192.168.1.41:554/cam/realmonitor?channel=1&subtype=0'.format(username, password)
#
#     # Create camera widgets
#     print('Creating Camera Widgets...')
#     zero = CameraWidget(screen_width//3, screen_height//3, camera0)
#     one = CameraWidget(screen_width//3, screen_height//3, camera1)
#     two = CameraWidget(screen_width//3, screen_height//3, camera2)
#     three = CameraWidget(screen_width//3, screen_height//3, camera3)
#     four = CameraWidget(screen_width//3, screen_height//3, camera4)
#     five = CameraWidget(screen_width//3, screen_height//3, camera5)
#     six = CameraWidget(screen_width//3, screen_height//3, camera6)
#     seven = CameraWidget(screen_width//3, screen_height//3, camera7)
#
#     # Add widgets to layout
#     print('Adding widgets to layout...')
#     ml.addWidget(zero.get_video_frame(),0,0,1,1)
#     ml.addWidget(one.get_video_frame(),0,1,1,1)
#     ml.addWidget(two.get_video_frame(),0,2,1,1)
#     ml.addWidget(three.get_video_frame(),1,0,1,1)
#     ml.addWidget(four.get_video_frame(),1,1,1,1)
#     ml.addWidget(five.get_video_frame(),1,2,1,1)
#     ml.addWidget(six.get_video_frame(),2,0,1,1)
#     ml.addWidget(seven.get_video_frame(),2,1,1,1)
#
#     print('Verifying camera credentials...')
#
#     mw.show()
#
#     QtGui.QShortcut(QtGui.QKeySequence('Ctrl+Q'), mw, exit_application)
#
#     if(sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()
