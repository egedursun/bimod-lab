#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: get_api_item.py
#  Last Modified: 2024-08-02 11:55:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:59:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django import template

register = template.Library()


@register.filter
def get_api_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_api_ids(dictionary, key):
    item = dictionary.get(key)
    ids = []
    for i in item:
        ids.append(i.custom_api.id)
    return ids
