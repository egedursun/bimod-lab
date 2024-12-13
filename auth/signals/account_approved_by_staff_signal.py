#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: account_approved_by_staff_signal.py
#  Last Modified: 2024-10-23 17:48:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-23 17:48:30
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

from django.db.models.signals import (
    post_save
)

from django.dispatch import (
    receiver
)

from django.utils import timezone

from auth.models import Profile

from auth.utils import (
    send_accreditation_approval_email
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def send_approval_email(
    sender,
    instance,
    **kwargs
):
    if (
        instance.is_accredited_by_staff and
        instance.accreditation_email_sent_at is None
    ):
        logger.info(f"Accreditation email sent to the administrator candidate user.")

        send_accreditation_approval_email(
            email=instance.email
        )

        print(f"Accreditation email sent to the administrator candidate user.")

        instance.accreditation_email_sent_at = timezone.now()

        instance.save(
            update_fields=['accreditation_email_sent_at']
        )
