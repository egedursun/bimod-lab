#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_004_media_storages_create.py
#  Last Modified: 2024-11-18 20:49:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:49:44
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

from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.datasource_media_storages.utils import MediaManagerItemCategoriesNames
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__004_media_storages_create(
    metadata__assistants
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:
                # Image
                DataSourceMediaStorageConnection.objects.create(
                    assistant=assistant,
                    media_category=MediaManagerItemCategoriesNames.Image,
                    name=f"{assistant.name}'s Image File Storage {generate_random_object_id_string()}",
                    description=f"This is the default image file storage for the assistant {assistant.name}."
                )
                # Audio
                DataSourceMediaStorageConnection.objects.create(
                    assistant=assistant,
                    media_category=MediaManagerItemCategoriesNames.Audio,
                    name=f"{assistant.name}'s Audio File Storage {generate_random_object_id_string()}",
                    description=f"This is the default audio file storage for the assistant {assistant.name}."
                )
                # Video
                DataSourceMediaStorageConnection.objects.create(
                    assistant=assistant,
                    media_category=MediaManagerItemCategoriesNames.Video,
                    name=f"{assistant.name}'s Video File Storage {generate_random_object_id_string()}",
                    description=f"This is the default video file storage for the assistant {assistant.name}."
                )
                # Compressed
                DataSourceMediaStorageConnection.objects.create(
                    assistant=assistant,
                    media_category=MediaManagerItemCategoriesNames.Compressed,
                    name=f"{assistant.name}'s Compressed File Storage {generate_random_object_id_string()}",
                    description=f"This is the default compressed file storage for the assistant {assistant.name}."
                )
                # Code
                DataSourceMediaStorageConnection.objects.create(
                    assistant=assistant,
                    media_category=MediaManagerItemCategoriesNames.Code,
                    name=f"{assistant.name}'s Code File Storage {generate_random_object_id_string()}",
                    description=f"This is the default code file storage for the assistant {assistant.name}."
                )
                # Data
                DataSourceMediaStorageConnection.objects.create(
                    assistant=assistant,
                    media_category=MediaManagerItemCategoriesNames.Data,
                    name=f"{assistant.name}'s Data File Storage {generate_random_object_id_string()}",
                    description=f"This is the default data file storage for the assistant {assistant.name}."
                )
            except Exception as e:
                logger.error(f"Error while creating media storage connections for assistant {assistant.name}: {e}")
                continue

    except Exception as e:
        logger.error(f"Error while creating media storage connection: {e}")
        return False

    logger.info("action__004_media_storages_create completed successfully.")
    return True
