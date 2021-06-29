import cv2
from plate_extractor.image_to_crop import get_image_to_crop
from plate_extractor.crop_to_plate import get_crop_to_plate


# returns extracted plate from given image
def get_image_to_plate(image, show_extraction_process):
    plate_text = None
    image_crop = get_image_to_crop(image, show_extraction_process)

    if image_crop is not None:
        plate_text = get_crop_to_plate(image_crop, show_extraction_process)

        if show_extraction_process:
            # displaying cropped part
            cv2.imshow('Cropped', image_crop)  # optional
    return plate_text


def __init__():
    # configurations
    image_path = "../test_data/image1.jpg"
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    show_extraction_process = True

    plate_number = get_image_to_plate(image, show_extraction_process)

    if show_extraction_process:
        # keeps image windows open
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(plate_number)


# __init__()
