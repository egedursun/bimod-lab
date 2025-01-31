#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: mtest_deepseek_r1.py
#  Last Modified: 2025-01-29 21:25:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-29 21:25:18
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import os
import replicate

REPLICATE_API_TOKEN = "r8_1NjgYRB9XLQ0yI7XMllU6fV5wkxQTb82WymoU"

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

prompt = [
    {
        "role": "system",
        "content": "You are a financial data analyst at a large bank."
    },
    {
        "role": "user",
        "content": "What are the most common financial analysis techniques?"
    }
]

for event in replicate.stream(
    "deepseek-ai/deepseek-r1",
    input={
        "prompt": str(prompt)
    }
):
    print(event, end="")
