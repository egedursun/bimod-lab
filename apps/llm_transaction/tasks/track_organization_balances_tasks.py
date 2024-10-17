#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: track_organization_balances_tasks.py
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
#
#
#
import logging

from celery import shared_task

from apps.llm_transaction.models import OrganizationBalanceSnapshot
from apps.organization.models import Organization


logger = logging.getLogger(__name__)


@shared_task
def track_organization_balances():
    all_orgs = Organization.objects.all()
    for org in all_orgs:
        ss = OrganizationBalanceSnapshot(organization=org, balance=org.balance)
        ss.save()
    logger.info(f"Organization balances were tracked.")
    return True
