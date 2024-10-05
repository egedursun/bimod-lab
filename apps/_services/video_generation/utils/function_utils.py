#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: function_utils.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
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


from uuid import uuid4


def generate_save_name(extension):
    try:
        generated_uuid = str(uuid4())
        additional_uuid = str(uuid4())
    except Exception as e:
        print(f"[VideoGenerationExecutor.generate_save_name] Error occurred while generating the save name: {str(e)}")
        return None
    print(f"[VideoGenerationExecutor.generate_save_name] Save name: {generated_uuid}_{additional_uuid}.{extension}")
    return f"{generated_uuid}_{additional_uuid}.{extension}"
