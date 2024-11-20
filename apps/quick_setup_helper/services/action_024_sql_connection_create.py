#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_024_sql_connection_create.py
#  Last Modified: 2024-11-18 22:27:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:27:08
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
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__024_sql_connection_create(
    metadata__user,
    metadata__organization,
    metadata__assistants,
    response__internal_data_sources__sql_dbms_type,
    response__internal_data_sources__sql_host,
    response__internal_data_sources__sql_port,
    response__internal_data_sources__sql_database_name,
    response__internal_data_sources__sql_username,
    response__internal_data_sources__sql_password,
    is_read_only
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:

                SQLDatabaseConnection.objects.create(
                    assistant=assistant,
                    created_by_user=metadata__user,
                    name=f"Primary SQL Database for assistant {assistant.name} {generate_random_object_id_string()}",
                    description=f"This is the primary SQL Database connection for the assistant {assistant.name} and organization {metadata__organization.name}.",
                    dbms_type=response__internal_data_sources__sql_dbms_type,
                    host=response__internal_data_sources__sql_host,
                    port=response__internal_data_sources__sql_port,
                    database_name=response__internal_data_sources__sql_database_name,
                    username=response__internal_data_sources__sql_username,
                    password=response__internal_data_sources__sql_password,
                    is_read_only=is_read_only
                )

            except Exception as e:
                logger.error(f"Failed to create SQL connection for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__024_sql_connection_create: {str(e)}")
        return False

    logger.info("action__024_sql_connection_create completed successfully.")
    return True
