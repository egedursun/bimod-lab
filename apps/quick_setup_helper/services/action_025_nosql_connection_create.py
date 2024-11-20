#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_025_nosql_connection_create.py
#  Last Modified: 2024-11-18 22:27:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:27:22
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
from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__025_nosql_connection_create(
    metadata__user,
    metadata__organization,
    metadata__assistants,
    response__internal_data_sources__nosql_db_type,
    response__internal_data_sources__nosql_host,
    response__internal_data_sources__nosql_bucket_name,
    response__internal_data_sources__nosql_username,
    response__internal_data_sources__nosql_password,
    is_read_only
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:

                NoSQLDatabaseConnection.objects.create(
                    assistant=assistant,
                    created_by_user=metadata__user,
                    name=f"Primary NoSQL Database for assistant {assistant.name} {generate_random_object_id_string()}",
                    description=f"This is the primary NoSQL Database connection for the assistant {assistant.name} and organization {metadata__organization.name}.",
                    nosql_db_type=response__internal_data_sources__nosql_db_type,
                    host=response__internal_data_sources__nosql_host,
                    bucket_name=response__internal_data_sources__nosql_bucket_name,
                    username=response__internal_data_sources__nosql_username,
                    password=response__internal_data_sources__nosql_password,
                    is_read_only=is_read_only
                )

            except Exception as e:
                logger.error(f"Failed to create NoSQL connection for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__025_nosql_connection_create: {str(e)}")
        return False

    logger.info("action__025_nosql_connection_create completed successfully.")
    return True
