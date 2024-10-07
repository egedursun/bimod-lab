#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: function_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from io import BytesIO

import qrcode
import tiktoken
from django.core.files.base import ContentFile
from django.template.loader import render_to_string


def calculate_number_of_tokens(encoding_engine, text):
    # Tokenize the text
    encoding = tiktoken.get_encoding(encoding_engine)
    tokens = encoding.encode(str(text))
    return len(tokens)


def calculate_llm_cost(model, number_of_tokens):
    from apps.llm_transaction.utils import LLMCostsPerMillionTokens

    costs = LLMCostsPerMillionTokens.OPENAI_GPT_COSTS[model]
    tokens_divided_by_million = number_of_tokens / 1_000_000
    apx_input_cost = (tokens_divided_by_million / 2) * costs["input"]
    apx_output_cost = (tokens_divided_by_million / 2) * costs["output"]
    llm_cost = (apx_input_cost + apx_output_cost)
    return llm_cost


def calculate_internal_service_cost(llm_cost, tool_service_fee_absolute_rate=0.000000):
    from apps.llm_transaction.utils import SERVICE_PROFIT_MARGIN
    # add the tool service fee rate
    bare_amount = llm_cost * SERVICE_PROFIT_MARGIN
    bare_amount += tool_service_fee_absolute_rate
    return bare_amount


def calculate_tax_cost(internal_service_cost):
    from apps.llm_transaction.utils import VAT_TAX_RATE
    tax_cost = internal_service_cost * VAT_TAX_RATE
    return tax_cost


def calculate_billable_cost(internal_service_cost, tax_cost):
    return internal_service_cost + tax_cost


def calculate_total_cost(llm_cost, billable_cost):
    return llm_cost + billable_cost


def sum_costs(transactions):
    llm_cost = 0
    internal_service_cost = 0
    tax_cost = 0
    total_cost = 0
    billable_cost = 0
    for transaction in transactions:
        llm_cost += transaction.llm_cost
        internal_service_cost += transaction.internal_service_cost
        tax_cost += transaction.tax_cost
        total_cost += transaction.total_cost
        billable_cost += transaction.total_billable_cost
    return {
        "llm_cost": llm_cost, "internal_service_cost": internal_service_cost, "tax_cost": tax_cost,
        "total_cost": total_cost, "total_billable_cost": billable_cost,
    }


def barcode_generator(hashed_string):
    try:
        img = qrcode.make(hashed_string)
        # Save to BytesIO object
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
    except Exception as e:
        print(["utils.barcode_generator]: There has been an error generating the barcode", e])
        return None
    # Convert BytesIO to Django ContentFile
    return ContentFile(buffer.getvalue(), name=f"QR_{hashed_string}.png")


def invoice_paper_generator(invoice_object, barcode_data):
    import base64
    organization = invoice_object.organization
    user = invoice_object.responsible_user
    # convert ContentFile to bytes
    barcode_data = barcode_data.file
    # convert barcode data to a base64 string
    barcode_data = base64.b64encode(barcode_data.getvalue()).decode('utf-8')
    # Render HTML template with data
    try:
        # Render the HTML content using the Django template and the invoice object
        html_content = render_to_string('llm_transaction/invoices/invoice_skeleton.html',
                                        {
                                            'invoice': invoice_object, 'organization': organization, 'user': user,
                                            'barcode_data': barcode_data,
                                        })
        print(["utils.invoice_paper_generator]: HTML content", html_content])
        # Create a Django ContentFile with the HTML content
        file_content = ContentFile(html_content.encode('utf-8'))
        # Define the filename
        filename = f"invoice_{str(invoice_object.invoice_number)}.html"
        print("[utils.invoice_paper_generator]: Filename", filename)
    except Exception as e:
        print("[utils.invoice_paper_generator]: There has been an error generating the invoice PDF", e)
        return None, None
    return filename, file_content
