#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: email_announcement_signals.py
#  Last Modified: 2024-10-23 18:13:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-23 18:13:03
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.db.models.signals import post_save
from django.dispatch import receiver

from auth.models import BimodEmailAnnouncement, Profile
from auth.utils import send_announcement_email


@receiver(post_save, sender=BimodEmailAnnouncement)
def announcement_email_signal(sender, instance, created, **kwargs):
    if created:
        all_user_emails = list(Profile.objects.values_list('email', flat=True))
        send_announcement_email(
            recipient_emails=all_user_emails, title_raw=instance.title_raw, body_raw=instance.body_raw
        )
        print(f"Announcement email sent to {len(all_user_emails)} users.")
    return
