#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

STATUSES_FOR_SUPPORT_TICKETS = [
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('closed', 'Closed'),
    ('resolved', 'Resolved'),
]

PRIORITY_CATEGORY_OF_SUPPORT_TICKETS = [
    ('recommendation', 'Recommendation'),
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
]

SUPPORT_TICKET_SYSTEM_ADMIN_LIST = ['title', 'status', 'priority', 'created_at']
SUPPORT_TICKET_SYSTEM_ADMIN_FILTER = ['status', 'priority']
SUPPORT_TICKET_SYSTEM_ADMIN_SEARCH = ['title', 'issue_description']

SUPPORT_TICKET_RESPONSE_ADMIN_LIST = ['ticket', 'user', 'created_at']
SUPPORT_TICKET_RESPONSE_ADMIN_SEARCH = ['ticket__title', 'response']


class TicketStatusPriorityMapScoreNames:
    OPEN = 3
    IN_PROGRESS = 2
    RESOLVED = 1
    CLOSED = 0


TICKET_STATUS_PRIORITY_MAP = {
    'open': TicketStatusPriorityMapScoreNames.OPEN,
    'in_progress': TicketStatusPriorityMapScoreNames.IN_PROGRESS,
    'resolved': TicketStatusPriorityMapScoreNames.RESOLVED,
    'closed': TicketStatusPriorityMapScoreNames.CLOSED
}

MAXIMUM_TICKET_FREQUENCY_ONCE_EVERY_HOURS_PER_USER = 12
