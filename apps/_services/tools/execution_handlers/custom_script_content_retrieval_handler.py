#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: custom_script_content_retrieval_handler.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: custom_script_content_retrieval_handler.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:19
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.multimodality.mm_scripts_content_retriever import CustomScriptsContentRetriever
from apps.mm_scripts.models import CustomScriptReference


def retrieve_script_content(custom_script_reference_id):
    script_reference = CustomScriptReference.objects.filter(id=custom_script_reference_id).first()
    print(
        f"[custom_script_content_retrieval_handler.retrieve_script_content] Retrieving the script content: {script_reference.custom_script.name}.")
    try:
        executor = CustomScriptsContentRetriever(script=script_reference.custom_script,
                                                 context_organization=script_reference.assistant.organization,
                                                 context_assistant=script_reference.assistant)
        response = executor.retrieve_custom_script_content()
    except Exception as e:
        error = (f"[custom_script_content_retrieval_handler.retrieve_script_content] Error occurred while retrieving "
                 f"the script content: {str(e)}")
        return error
    print(f"[custom_script_content_retrieval_handler.retrieve_script_content] Script content retrieved successfully.")
    return response
