#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-31 05:36:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 13:14:20
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

logger = logging.getLogger(__name__)


def is_final_output(response: str):
    from apps.core.formica.utils import (
        FormicaGoogleFormsQuestionTypesNames
    )

    count = 0

    for specifier in FormicaGoogleFormsQuestionTypesNames.Config_OutputFinalResponseSpecifiers.as_list():

        if specifier in response:
            count += 1

    if count == len(FormicaGoogleFormsQuestionTypesNames.Config_OutputFinalResponseSpecifiers.as_list()):
        logger.info(f"Final output specifier found in response")

        return True

    logger.info(f"Final output specifier not found in response")

    return False
