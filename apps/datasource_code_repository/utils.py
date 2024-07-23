import random

import wonderwords


def generate_random_words():
    # use a library to generate a random chat name
    chat_name_1 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories = ["noun"],
        regex=r"^[a-zA-Z]+$"
    )
    chat_name_2 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories = ["noun"],
        regex=r"^[a-zA-Z]+$"
    )
    chat_name_3 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories = ["noun"],
        regex=r"^[a-zA-Z]+$"
    )
    chat_name_1 = chat_name_1.capitalize()
    chat_name_2 = chat_name_2.capitalize()
    chat_name_3 = chat_name_3.capitalize()
    random_digit_string = str(random.randint(1_000_000, 9_999_999))
    return "".join([chat_name_1, chat_name_2, chat_name_3, random_digit_string])

def convert_given_name_to_class_name(given_name: str):
    given_name_alnum = ""
    for char in given_name:
        if char.isalnum() and char not in [" ", "_", "-", ".", ":", ";", ",", "'", '"', "!", "@", "#", "$", "%", "^",
                                           "&", "*", "(", ")", "+", "=", "{", "}", "[", "]", "<", ">", "?", "/", "\\",
                                           "|", "`", "~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            given_name_alnum += char
    given_name_alnum_list = given_name_alnum.lower().capitalize()
    return given_name_alnum_list


def generate_class_name(connection):
    # Generate random words
    given_class_name_generation = convert_given_name_to_class_name(connection.name)
    randoms = generate_random_words()
    return f"{given_class_name_generation}{randoms}"
