#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: convert_file_size.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django import template

from apps.datasource_media_storages.utils import UNIT_BYTES_THOUSAND

register = template.Library()


@register.filter
def convert_file_size(byte_size):
    k_bytes = (byte_size / UNIT_BYTES_THOUSAND)
    str_k_bytes = f'{k_bytes:.2f} KB'
    return str_k_bytes
