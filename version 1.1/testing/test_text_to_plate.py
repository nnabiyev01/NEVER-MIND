""" Unit testing of plate_extractor/text_to_plate.py """

# import text_to_plate.py
from plate_extractor.text_to_plate import get_plate


def test():
    image_text = "dfkASj15Adj10-AA-102skj12 sBC-23-324"
    assert get_plate(image_text) == "10 AA 102"
    image_text = "90\nBC 341insert text"
    assert get_plate(image_text) == "90 BC 341"
    image_text = "G6 02 SS5"
    assert get_plate(image_text) == "66 OZ 555"
    image_text = "jdk10-BJ 205"
    assert get_plate(image_text) == "10 BJ 205"
    image_text = "\n50-66 927"
    assert get_plate(image_text) == "50 GG 927"

    image_text = "23 GDC 203"
    assert get_plate(image_text) == ""
    image_text = "391 AA 11"
    assert get_plate(image_text) == ""
    image_text = "Az dk\n\t10-AA  23"
    assert get_plate(image_text) == ""

    print("all tests successful")


test()
