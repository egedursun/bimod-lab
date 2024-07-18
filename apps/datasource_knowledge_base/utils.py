import random
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
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


def generate_chat_history_class_name():
    # Generate random words
    randoms = generate_random_alphanumeric()
    return f"ChatHistory{randoms}"


def generate_document_uri(base_dir, document_name, file_type):
    return f"{base_dir}{document_name.split('.')[0]}_{str(random.randint(1_000_000, 9_999_999))}.{file_type}"


def generate_random_alphanumeric(numeric_component=True):
    chat_name_1 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories=["noun"],
        regex=r"^[a-zA-Z]+$"
    )
    chat_name_2 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories=["noun"],
        regex=r"^[a-zA-Z]+$"
    )
    chat_name_3 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories=["noun"],
        regex=r"^[a-zA-Z]+$"
    )
    chat_name_4 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories=["noun"],
        regex=r"^[a-zA-Z]+$"
    )
    numeric = "0123456789"
    alpha_string = (chat_name_1.capitalize() + chat_name_2.capitalize() + chat_name_3.capitalize() +
                    chat_name_4.capitalize())
    numeric_string = "".join(random.choice(numeric) for _ in range(8))
    if numeric_component:
        return f"{alpha_string}{numeric_string}"
    else:
        return alpha_string


if __name__ == "__main__":
    pass
