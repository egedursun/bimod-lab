#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_smart_contract_query.py
#  Last Modified: 2024-11-13 05:12:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:12:21
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.smart_contracts.utils import SmartContractCategoriesNames, SmartContractTemplateNames


def verify_smart_contract_generation_query_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Smart Contract
            Query tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    ps = content.get("parameters")
    if "wallet_id" not in ps:
        return """
            The 'wallet_id' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Smart Contract Query tool. Please make sure you are defining the 'wallet_id' field in the 'parameters'
            field in the tool_usage_json.
        """
    if type(ps["wallet_id"]) is not int:
        return """
            The 'wallet_id' field in the 'parameters' field in the tool_usage_json must be an integer. Please make sure you
            are defining the 'wallet_id' field in the 'parameters' field in the tool_usage_json as an integer.
        """
    if "nickname" not in ps:
        return """
            The 'nickname' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Smart Contract Query tool. Please make sure you are defining the 'nickname' field in the 'parameters'
            field in the tool_usage_json.
        """
    if "description" not in ps:
        return """
            The 'description' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Smart Contract Query tool. Please make sure you are defining the 'description' field in the 'parameters'
            field in the tool_usage_json.
        """
    if "category" not in ps:
        return """
            The 'category' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Smart Contract Query tool. Please make sure you are defining the 'category' field in the 'parameters'
            field in the tool_usage_json.
        """
    if ps["category"] not in SmartContractCategoriesNames.as_list():
        return """
            The 'category' field in the 'parameters' field in the tool_usage_json is not valid. Please make sure you are defining
            a valid 'category' field in the 'parameters' field in the tool_usage_json.
        """
    if "contract_template" not in ps:
        return """
            The 'contract_template' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Smart Contract Query tool. Please make sure you are defining the 'contract_template' field in the 'parameters'
            field in the tool_usage_json.
        """
    if ps["contract_template"] not in SmartContractTemplateNames.Custom.as_list():
        return """
            The 'contract_template' field in the 'parameters' field in the tool_usage_json is not valid. Please make sure you are defining
            a valid 'contract_template' field in the 'parameters' field in the tool_usage_json.
        """
    if "creation_prompt" not in ps:
        return """
            The 'creation_prompt' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Smart Contract Query tool. Please make sure you are defining the 'creation_prompt' field in the 'parameters'
            field in the tool_usage_json.
        """
    if "maximum_gas_limit" not in ps:
        return """
            The 'maximum_gas_limit' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Smart Contract Query tool. Please make sure you are defining the 'maximum_gas_limit' field in the 'parameters'
            field in the tool_usage_json.
        """
    if type(ps["maximum_gas_limit"]) is not int:
        return """
            The 'maximum_gas_limit' field in the 'parameters' field in the tool_usage_json must be an integer. Please make sure you
            are defining the 'maximum_gas_limit' field in the 'parameters' field in the tool_usage_json as an integer.
        """
    if "gas_price_gwei" not in ps:
        return """
            The 'gas_price_gwei' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Smart Contract Query tool. Please make sure you are defining the 'gas_price_gwei' field in the 'parameters'
            field in the tool_usage_json.
        """
    if type(ps["gas_price_gwei"]) is not int:
        return """
            The 'gas_price_gwei' field in the 'parameters' field in the tool_usage_json must be an integer. Please make sure you
            are defining the 'gas_price_gwei' field in the 'parameters' field in the tool_usage_json as an integer.
        """
    return None
