#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging
import random
import warnings

from apps.core.vector_operations.vector_document.utils import (
    SupportedDocumentTypesNames
)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import wonderwords

logger = logging.getLogger(__name__)


def build_name_string_for_randomized():
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

    chat_name_1 = chat_name_1.capitalize()
    chat_name_2 = chat_name_2.capitalize()
    chat_name_3 = chat_name_3.capitalize()

    random_digit_string = str(random.randint(1_000_000, 9_999_999))

    return "".join([
        chat_name_1,
        chat_name_2,
        chat_name_3,
        random_digit_string
    ])


def convert_given_name_to_class_name(given_name: str):
    given_name_alnum = ""
    for char in given_name:
        if char.isalnum() and char not in [
            " ",
            "_",
            "-",
            ".",
            ":",
            ";",
            ",",
            "'",
            '"',
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "+",
            "=",
            "{",
            "}",
            "[",
            "]",
            "<",
            ">",
            "?",
            "/",
            "\\",
            "|",
            "`",
            "~",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0"
        ]:
            given_name_alnum += char

    given_name_alnum_list = given_name_alnum.lower().capitalize()

    return given_name_alnum_list


def build_weaviate_class_name(connection):
    given_class_name_generation = convert_given_name_to_class_name(
        connection.name
    )

    randoms = build_name_string_for_randomized()

    return f"{given_class_name_generation}{randoms}"


def build_weaviate_intra_memory_class_name():
    randoms = build_random_alphanumeric_string()
    return f"ChatHistory{randoms}"


def generate_document_uri(
    base_dir,
    document_name,
    file_type
):
    return f"{base_dir}{document_name.split('.')[0]}_{str(random.randint(
        1_000_000,
        9_999_999
    ))}.{file_type}"


def build_random_alphanumeric_string(numeric_component=True):
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

    alpha_string = (
        chat_name_1.capitalize() +
        chat_name_2.capitalize() +
        chat_name_3.capitalize() +
        chat_name_4.capitalize()
    )

    numeric_string = "".join(random.choice(numeric) for _ in range(8))

    if numeric_component:
        return f"{alpha_string}{numeric_string}"

    else:
        return alpha_string


def document_loader(
    file_path,
    file_type
):
    from apps.datasource_knowledge_base.tasks import (
        load_pdf_content,
        load_html_content,
        load_csv_content,
        load_docx_content,
        load_ipynb_content,
        load_json_content,
        load_xml_content,
        load_txt_content,
        load_md_content,
        load_rtf_content,
        load_odt_content,
        load_pptx_content,
        load_xlsx_content
    )

    logger.info(f"Document is being loaded: {file_path}")
    d = None

    if file_type == SupportedDocumentTypesNames.PDF:
        d = load_pdf_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.HTML:
        d = load_html_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.CSV:
        d = load_csv_content(uri=file_path)

    elif file_type == SupportedDocumentTypesNames.DOCX:
        d = load_docx_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.IPYNB:
        d = load_ipynb_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.JSON:
        d = load_json_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.XML:
        d = load_xml_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.TXT:
        d = load_txt_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.MD:
        d = load_md_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.RTF:
        d = load_rtf_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.ODT:
        d = load_odt_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.POWERPOINT:
        d = load_pptx_content(path=file_path)

    elif file_type == SupportedDocumentTypesNames.XLSX:
        d = load_xlsx_content(path=file_path)

    else:
        pass

    result = d
    logger.info(f"Document Loader: {result}")

    return result
