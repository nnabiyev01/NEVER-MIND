import pytesseract
from text_to_plate import get_plate


# reading the plate number based on crop
# makes use of text_to_plate.py
def read_plate_number(given_crop, show_extraction_process):
    # required in Windows
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    # string_whitelist = "C:/Program Files/Tesseract-OCR/tessdata/eng.user-patterns"

    # configurations
    character_whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- "
    default_config = f"-c tessedit_char_whitelist={character_whitelist}"

    arg_default = [given_crop, 'eng', default_config]
    arg_psm_8 = [given_crop, 'eng', f"--psm 8 {default_config}"]
    arg_psm_11 = [given_crop, "eng", f"--psm 11 {default_config}"]

    # extracting with default (no psm), psm 8 and psm 11
    # priority: psm 11 > psm 8 > default
    opt1, opt1_data = get_ocr_text(arg_psm_11), get_ocr_data(arg_psm_11)
    opt2, opt2_data = get_ocr_text(arg_psm_8), get_ocr_data(arg_psm_8)
    opt3, opt3_data = get_ocr_text(arg_default), get_ocr_data(arg_default)

    # check the result for each option (optional)
    if show_extraction_process:
        print(opt1_data)
        print(opt2_data)
        print(opt3_data)

    # assigning, returning dict values
    dict_of_options = {opt1: get_plate(opt1), opt2: get_plate(opt2), opt3: get_plate(opt3)}
    return dict_of_options


# returns image_to_string result for given parameters
def get_ocr_text(args):
    return pytesseract.image_to_string(args[0], lang=args[1], config=args[2])


# returns image_to_data result for given parameters
def get_ocr_data(args):
    return pytesseract.image_to_data(args[0], lang=args[1], config=args[2], output_type='data.frame')


# compares and finds the correct plate text from given options
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


# returns plate obtained using OCR
def get_crop_to_plate(given_crop, show_extraction_process):
    result_dict = read_plate_number(given_crop, show_extraction_process)
    extraction, plate_text, wrong_extractions = find_the_correct_text_option(result_dict)

    # optional
    if show_extraction_process:
        if plate_text:
            print("---Extracted Text---\n" + extraction)
            print("---Plate Text---\n" + plate_text)
        else:
            print("---Extracted Text---\n" + '  1st<-->2nd  '.
                  join(str(x) for x in wrong_extractions))
            print("---Plate Text---\n" + plate_text)

    return plate_text
