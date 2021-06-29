""" Testing using images in test_data """

import os
import cv2
# import image_to_plate.py
from plate_extractor.image_to_plate import get_image_to_plate


# loads all images from the given folder
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


# depending on the size of test data, testing could take longer
# expect around 0.75 per image
def test():
    images = load_images_from_folder("../test_data")
    extracted_plates = []

    for image in images:
        extracted_plate_text = get_image_to_plate(image, False)
        if extracted_plate_text is not None and extracted_plate_text != "":
            extracted_plates.append(extracted_plate_text)

    success_rate = len(extracted_plates) / len(images)
    print(f"success rate was: {success_rate}%")
    print(f"extracted plate are: {extracted_plates}")


test()
