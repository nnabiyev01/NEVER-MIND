import pytesseract
from PIL import Image

# import the plate_extractor
from plate_extractor import get_plate

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

img = Image.open('plate_sample.jpg')
image_text = pytesseract.image_to_string(img)




# all data read from the image
print("-----Original Image Text-----")
print(image_text)

# plate number extracted from the image
# empty array if no plate number was found
print("-----Extracted Plate Number-----")
print(get_plate(image_text))
