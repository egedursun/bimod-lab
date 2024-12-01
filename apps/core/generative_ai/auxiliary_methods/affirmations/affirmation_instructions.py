#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: affirmation_instructions.py
#  Last Modified: 2024-10-08 23:46:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-08 23:46:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

GENERIC_AFFIRMATION_PROMPT = f"""

    **Affirmation Prompt**
    - DO NOT ASK QUESTIONS TO ME. YOU ARE A ZERO-SHOT MODEL, PEOPLE WON'T CHAT WITH YOU, JUST PROVIDE YOUR BEST ANSWER.
"""

MACHINE_LEARNING_AFFIRMATION_PROMPT = f"""

    **Machine Learning Affirmation Prompt**
    - NEVER USE KERAS AND TENSORFLOW. ALWAYS USE PYTORCH. ALWAYS USE THE MODEL THAT IS SHARED WITH YOU, DO NOT DEVELOP MODELS YOURSELF.
    - You will receive data and the ".pth" model for prediction. You will use the model to predict the data and provide the results.
"""
