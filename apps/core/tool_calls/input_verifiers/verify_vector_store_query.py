#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_vector_store_query.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection


def verify_vector_store_query_content(content: dict):

    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Knowledge
            Base Query Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """

    ps = content.get("parameters")

    if "query" not in ps:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Knowledge Base Query Execution tool. Please make sure you are defining the 'query' field in the
            parameters field of the tool_usage_json.
        """

    if "alpha" not in ps:
        return """
            The 'alpha' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Knowledge Base Query Execution tool. Please make sure you are defining the 'alpha' field in the
            parameters field of the tool_usage_json.
        """

    c = DocumentKnowledgeBaseConnection.objects.get(
        id=ps.get(
            "knowledge_base_connection_id"
        )
    )

    if not c:
        return f"""
            The Knowledge Base Connection with the ID: {c.id} does not exist in the system.
            Please make sure you are passing a valid knowledge base connection ID.
        """

    return None
