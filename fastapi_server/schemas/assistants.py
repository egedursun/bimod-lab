#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistant.py
#  Last Modified: 2025-02-01 21:57:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-02-01 21:57:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from pydantic import BaseModel


class AssistantCreate(BaseModel):
    organization_id: int
    llm_model_id: int
    name: str
    description: str = ""
    instructions: str = "You are a helpful assistant."
    response_template: str = ""
    audience: str = "Standard"
    tone: str = "Standard"
    response_language: str = "auto"
    max_retry_count: int = 3
    tool_max_attempts_per_instance: int = 3
    tool_max_chains: int = 3
    glossary: dict = {}
    time_awareness: bool = True
    place_awareness: bool = True
    context_overflow_strategy: str = "forget"
    max_context_messages: int = 25
    image_generation_capability: bool = True
    multi_step_reasoning_capability_choice: str = "none"
    ner_integration: int = None
    is_beamguard_active: bool = True
    created_by_user_id: int
    last_updated_by_user_id: int
