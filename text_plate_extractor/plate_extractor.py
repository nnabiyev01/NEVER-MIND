from re import compile

# number(s), -, 2 characters, -, number(s)
# e.g: 10-BD-100
default_format = compile('^[0-9]+[ -][a-zA-Z][a-zA-Z][ -][0-9]+$')
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
    text_rows = given_text.split('\n')
    extracted_plates = []

    for i in range(len(text_rows)):
        row_result = contains_format(text_rows[i])
        if row_result != "":
            extracted_plates.append(row_result)

    return list_to_string(extracted_plates).replace("-", " ")


# converts a list into string
def list_to_string(list_sample):
    string = ""
    for ele in list_sample:
        string += ele
    return string
