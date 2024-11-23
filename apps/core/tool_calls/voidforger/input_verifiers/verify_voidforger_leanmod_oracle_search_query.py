#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_voidforger_leanmod_oracle_search_query.py
#  Last Modified: 2024-11-16 00:37:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:37:25
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def verify_voidforger_leanmod_oracle_search_query_content(content: dict):

    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the
            Voidforger Leanmod Oracle Search tool. Please make sure you are defining the 'parameters' field in the
            tool_usage_json.
        """

    ps = content.get("parameters")

    if "query" not in ps:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Voidforger Leanmod Oracle Search tool. Please make sure you are defining the 'query' field in
            the parameters field of the tool_usage_json.
        """

    return None
