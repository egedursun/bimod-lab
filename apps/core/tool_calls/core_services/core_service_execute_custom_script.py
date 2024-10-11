#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: core_service_execute_custom_script.py
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


from apps.core.flexible_modalities.custom_script_executor import CustomScriptsContentRetriever
from apps.mm_scripts.models import CustomScriptReference


def run_execute_custom_script(ref_id):
    ref = CustomScriptReference.objects.filter(id=ref_id).first()
    try:
        xc = CustomScriptsContentRetriever(script=ref.custom_script, context_organization=ref.assistant.organization,
                                           context_assistant=ref.assistant)
        output = xc.retrieve_custom_script_content()
    except Exception as e:
        error_msg = f"Error occurred while retrieving the script content: {str(e)}"
        return error_msg
    return output
