#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: notification_filters.py
#  Last Modified: 2024-10-20 18:09:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 18:11:25
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django import template

register = template.Library()


@register.filter
def unread_notifications(
    user_notifications,
    user
):
    unread_items = []

    for item in user_notifications:

        if user not in item.readers.all():
            unread_items.append(item)

    return unread_items
