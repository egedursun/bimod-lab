#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: markdown_extras.py
#  Last Modified: 2024-08-02 12:17:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:05:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markdownify')
def markdownify(text):
    return mark_safe(markdown.markdown(text))
