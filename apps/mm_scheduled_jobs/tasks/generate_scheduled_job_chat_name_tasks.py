#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: generate_scheduled_job_chat_name_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
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
from uuid import uuid4

from slugify import slugify

logger = logging.getLogger(__name__)


def generate_scheduled_job_chat_name(scheduled_job_name):
    uuid_1 = str(uuid4())
    uuid_2 = str(uuid4())
    logger.info(f"Generating Chat Name for Scheduled Job: {scheduled_job_name}")

    return f"{slugify(scheduled_job_name)} - {uuid_1} - {uuid_2}"
