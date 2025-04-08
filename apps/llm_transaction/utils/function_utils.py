#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#


import logging
from io import BytesIO

import qrcode
import tiktoken

from django.core.files.base import (
    ContentFile
)

from django.template.loader import (
    render_to_string
)

from apps.core.internal_cost_manager.costs_map import (
    TOOL_NAME_TO_COST_MAP
)

from config.settings import (
    SERVICE_COST_INPUT_PER_MILLION,
    SERVICE_COST_OUTPUT_PER_MILLION,
    SERVICE_TAX_RATE
)

logger = logging.getLogger(__name__)


def calculate_total_tokens(
    encoding_engine,
    text
):
    try:
        encoding = tiktoken.get_encoding(
            encoding_engine
        )

        tokens = encoding.encode(str(text))

    except Exception as e:
        raise ValueError(f"Error occurred while tokenizing the text: {str(e)}")

    return len(tokens)


def calculate_tool_cost(
    transaction_source
):
    tool_cost = float(
        TOOL_NAME_TO_COST_MAP[transaction_source]
    ) or 0.000000

    tool_cost_after_tax = ((tool_cost * SERVICE_TAX_RATE) + tool_cost)
    return tool_cost_after_tax


def calculate_billable_cost_from_raw(
    text,
    token_type,
):
    total_tokens = calculate_total_tokens(
        encoding_engine="cl100k_base",
        text=text
    )

    return calculate_billable_cost(
        total_tokens=total_tokens,
        token_type=token_type
    )


def calculate_billable_cost(
    total_tokens,
    token_type,
):
    from apps.llm_transaction.utils import (
        LLMTokenTypesNames
    )

    service_cost_input = SERVICE_COST_INPUT_PER_MILLION
    service_cost_output = SERVICE_COST_OUTPUT_PER_MILLION
    M_TOKENS = 1_000_000

    if token_type == LLMTokenTypesNames.INPUT:
        cost_per_token = service_cost_input

    elif token_type == LLMTokenTypesNames.OUTPUT:
        cost_per_token = service_cost_output

    else:
        cost_per_token = service_cost_output

    total_cost = ((total_tokens / M_TOKENS) * cost_per_token)
    total_cost_with_tax = ((total_cost * SERVICE_TAX_RATE) + total_cost)

    return total_cost_with_tax


def sum_costs(transactions):
    billable_cost = 0

    for transaction in transactions:
        billable_cost += transaction.total_billable_cost

    return {
        "total_billable_cost": billable_cost,
    }


def barcode_generator(hashed_string):
    logger.info(f"Generating barcode for hashed string: {hashed_string}")

    try:
        img = qrcode.make(
            hashed_string
        )

        buffer = BytesIO()

        img.save(
            buffer,
            format="PNG"
        )

        buffer.seek(0)

    except Exception as e:
        logger.error(f"Error occurred while generating barcode: {str(e)}")
        return None

    return ContentFile(
        buffer.getvalue(),
        name=f"QR_{hashed_string}.png"
    )


def invoice_paper_generator(
    invoice_object,
    barcode_data
):
    logger.info(f"Generating invoice: {invoice_object.invoice_number}")

    import base64

    org = invoice_object.organization
    user = invoice_object.responsible_user

    barcode_data = barcode_data.file

    barcode_data = base64.b64encode(
        barcode_data.getvalue()
    ).decode('utf-8')

    try:
        html_content = render_to_string(
            'llm_transaction/invoices/invoice_skeleton.html',
            {
                'invoice': invoice_object,
                'organization': org,
                'user': user,
                'barcode_data': barcode_data,
            }
        )

        file_content = ContentFile(
            html_content.encode('utf-8')
        )

        filename = f"invoice_{str(invoice_object.invoice_number)}.html"

    except Exception as e:
        logger.error(f"Error occurred while generating invoice: {str(e)}")

        return None, None

    return filename, file_content
