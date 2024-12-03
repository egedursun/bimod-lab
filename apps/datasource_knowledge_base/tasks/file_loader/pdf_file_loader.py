#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: load_pdf_helper_tasks.py
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

import fitz
import pdfplumber

from langchain_community.document_loaders import (
    PyPDFLoader
)

logger = logging.getLogger(__name__)


def load_pdf_content(path: str):
    clean_doc = {
        "page_content": "",
        "metadata": {}
    }

    # ATTEMPT 1: Attempt to load using PyPDFLoader
    clean_doc__pypdfloader = load_with_pypdfloader(path)
    performance_length__pypdfloader = len(clean_doc__pypdfloader["page_content"])

    # ATTEMPT 2: Fallback to PDFPlumber
    clean_doc__pdfplumber = load_pdf_with_pdfplumber(path)
    performance_length__pdfplumber = len(clean_doc__pdfplumber["page_content"])

    # ATTEMPT 3: Final fallback to PyMuPDF
    clean_doc__pymupdf = load_pdf_with_pymupdf(path)
    performance_length__pymupdf = len(clean_doc__pymupdf["page_content"])

    print(" | PyPDFLoader Performance:", performance_length__pypdfloader)
    print(" | PDFPlumber Performance:", performance_length__pdfplumber)
    print(" | PyMuPDF Performance:", performance_length__pymupdf)

    if (
        performance_length__pypdfloader > performance_length__pdfplumber and
        performance_length__pypdfloader > performance_length__pymupdf
    ):
        print("/ PyPDFLoader has the best performance.")
        clean_doc = clean_doc__pypdfloader

    elif (
        performance_length__pdfplumber > performance_length__pypdfloader and
        performance_length__pdfplumber > performance_length__pymupdf
    ):
        print("/ PDFPlumber has the best performance.")
        clean_doc = clean_doc__pdfplumber

    elif (
        performance_length__pymupdf > performance_length__pypdfloader and
        performance_length__pymupdf > performance_length__pdfplumber
    ):
        print("/ PyMuPDF has the best performance.")
        clean_doc = clean_doc__pymupdf

    return clean_doc


def load_with_pypdfloader(path: str):
    loader = PyPDFLoader(file_path=path)
    docs = loader.load()

    clean_doc = {
        "page_content": "",
        "metadata": {}
    }

    for doc in docs:
        pg_content = doc.page_content
        meta = doc.metadata

        clean_doc["page_content"] += pg_content
        clean_doc["metadata"] = meta

    return clean_doc


def load_pdf_with_pdfplumber(path: str):
    page_content = ""
    metadata = {}

    with pdfplumber.open(path) as pdf:
        metadata = pdf.metadata
        for page in pdf.pages:
            page_content += page.extract_text() or ""

    return {
        "page_content": page_content,
        "metadata": metadata
    }


def load_pdf_with_pymupdf(path: str):
    doc = fitz.open(path)
    page_content = ""

    metadata = doc.metadata or {}

    for page in doc:
        page_content += page.get_text()

    doc.close()

    return {
        "page_content": page_content,
        "metadata": metadata
    }
