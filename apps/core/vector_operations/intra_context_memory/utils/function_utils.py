#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: function_utils.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from apps.core.vector_operations.vector_document.utils import SupportedDocumentTypesNames
from apps.datasource_knowledge_base.tasks import load_pdf_content, load_html_content, load_csv_content, load_docx_content, \
    load_ipynb_content, load_json_content, load_xml_content, load_txt_content, load_md_content, load_rtf_content, \
    load_odt_content, load_pptx_content, load_xlsx_content


def document_loader(file_path, file_type):
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
    return result
