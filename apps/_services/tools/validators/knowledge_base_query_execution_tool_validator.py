#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: knowledge_base_query_execution_tool_validator.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#


from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection


def validate_knowledge_base_query_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Knowledge
            Base Query Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Knowledge Base Query Execution tool. Please make sure you are defining the 'query' field in the
            parameters field of the tool_usage_json.
        """
    if "alpha" not in parameters:
        return """
            The 'alpha' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Knowledge Base Query Execution tool. Please make sure you are defining the 'alpha' field in the
            parameters field of the tool_usage_json.
        """

    connection = DocumentKnowledgeBaseConnection.objects.get(id=parameters.get("knowledge_base_connection_id"))
    if not connection:
        return f"""
            The Knowledge Base Connection with the ID: {connection.id} does not exist in the system.
            Please make sure you are passing a valid knowledge base connection ID.
        """
    print(
        f"[knowledge_base_query_execution_tool_validator.validate_knowledge_base_query_execution_tool_json] Validation is successful.")
    return None
