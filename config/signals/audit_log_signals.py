#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: audit_log_signals.py
#  Last Modified: 2024-10-11 05:19:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-11 05:19:51
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib.admin.models import LogEntry
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import transaction

from apps.audit_logs.models import AuditLog
from config.utils.constant_utils import EXCLUDE_MODELS_FROM_AUDIT_LOGS


@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender in EXCLUDE_MODELS_FROM_AUDIT_LOGS:
        return

    with transaction.atomic():
        if created:
            if not hasattr(instance, 'id') or not instance.id:
                pass
            else:
                AuditLog.objects.create(action='create', model_name=sender.__name__, object_id=instance.id)
        else:
            if not hasattr(instance, 'id') or not instance.id:
                pass
            else:
                audit_log = AuditLog(action='update', model_name=sender.__name__, object_id=instance.id)
                if hasattr(instance, '_old_instance') and instance._old_instance:
                    audit_log.save_changes(instance._old_instance, instance)
                audit_log.save()


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender in EXCLUDE_MODELS_FROM_AUDIT_LOGS:
        return

    with transaction.atomic():
        if not hasattr(instance, 'id') or not instance.id:
            pass
        else:
            AuditLog.objects.create(action='delete', model_name=sender.__name__, object_id=instance.id)
