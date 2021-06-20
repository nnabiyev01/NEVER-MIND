from re import compile

# number(s), -, 2 characters, -, number(s)
# e.g: 10-BD-100
default_format = compile('^[0-9]+[ -][06a-zA-Z][06a-zA-Z][ -][0-9]+$')
default_format_length = 9


# checks if the given string matches the format
def matches_format(given_format, string):
    matched = given_format.match(string)
    return bool(matched)


# returns the found plate if part of the text matches the format
# returns empty string otherwise
def contains_format(string_sample, format_to_search=default_format,
                    format_length=default_format_length):
    string_row = list(string_sample)
    for i in range(len(string_row)):
        if len(string_row) - i >= format_length:
            part_to_search = list_to_string(string_row[i:(i+format_length)])

            if matches_format(format_to_search, part_to_search):
                return part_to_search
    return ""


# returns a list of plates of matching format from the given text
def get_plate(given_text):
    extraction = ""
    # grouping all extraction content on 1 line
    given_text = given_text.replace("\n", " ")

    result = contains_format(given_text)
    if result != "":
        extraction = result

    extraction = extraction.replace("-", " ")
    extraction = extraction.replace(extraction[3:5], filter_plate(extraction[3:5], letter_filters))
    return extraction


# converts a list into string
def list_to_string(list_sample):
    string = ""
    for ele in list_sample:
        string += ele
    return string


# letter filters are only used when changing the letter part the plate
# 00 AA 000 -> "AA" will be affected
letter_filters = [["0", "O"], ["6", "G"]]


# adjusts misread characters to predicted corrections
def filter_plate(given_text, filter_type):
    for i in range(len(filter_type)):
        given_text = given_text.replace(filter_type[i][0], filter_type[i][1])
    return given_text
