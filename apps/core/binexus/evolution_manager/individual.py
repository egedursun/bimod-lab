#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: individual.py
#  Last Modified: 2024-10-22 03:13:12
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 03:13:13
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
import uuid

from apps.binexus.models import (
    BinexusProcess,
    BinexusEliteAgent
)

from apps.core.binexus.evolution_manager import Chromosome

from apps.core.binexus.prompt_builders.binexus_individual_assignment_prompt_builders import (
    build_binexus_individual_assignment_prompt
)

from apps.core.binexus.prompts.binexus_individual_assignment_prompt import (
    binexus_individual_assignment_prompt_redacted
)

from apps.core.binexus.utils import (
    generate_random_elite_agent_name
)

from apps.core.generative_ai.gpt_openai_manager import (
    OpenAIGPTClientManager
)

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

from apps.llm_core.models import LLMCore
from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

logger = logging.getLogger(__name__)


class Individual:
    def __init__(
        self,
        process: BinexusProcess,
        llm_model: LLMCore,
        chromosome: Chromosome
    ):

        self.process: BinexusProcess = process
        self.llm_model: LLMCore = llm_model

        self.c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.llm_model
        )

        self.uuid_string = str(uuid.uuid4())
        self.chromosome: dict = chromosome
        self.assignment_content: str = self._create_assignment()
        self.fitness: float = -1

    def ascend_to_elite(self):
        try:
            new_elite_individual: BinexusEliteAgent = BinexusEliteAgent(
                binexus_process=self.process,
                agent_nickname=generate_random_elite_agent_name(),
                agent_prompt=binexus_individual_assignment_prompt_redacted(
                    process=self.process,
                    individual=self
                ),
                agent_temperature=self.chromosome.get(
                    Chromosome.GeneNames.TEMPERATURE, 0.5
                ),
                binexus_fitness_score=self.fitness,
                agent_chromosome_parameters=self.get_chromosome()
            )
            new_elite_individual.save()

            logger.info(f"New Elite Agent Ascended: {new_elite_individual.agent_nickname}")

            return True

        except Exception as e:
            logger.error(f"Error while ascending to elite: {e}")

            return False

    def get_fitness_score(self):
        return self.fitness

    def get_assignment_content(self):
        return self.assignment_content

    def _create_assignment(self):
        try:
            system_prompt = build_binexus_individual_assignment_prompt(
                process=self.process,
                individual=self
            )

            structured_messages = [
                {
                    "role": ChatRoles.SYSTEM,
                    "content": system_prompt
                }
            ]

            tx = LLMTransaction.objects.create(
                organization=self.process.organization,
                model=self.llm_model,
                responsible_user=self.process.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(system_prompt),
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.BINEXUS
            )

            tx.save()

            logger.info(f"[_create_assignment] Created system prompt LLM Transaction for Binexus Assignment Creation.")

            agent_temperature_value = self.chromosome.get(
                Chromosome.GeneNames.TEMPERATURE,
                0.5
            )

            llm_response = self.c.chat.completions.create(
                model=self.llm_model.model_name,
                messages=structured_messages,
                temperature=agent_temperature_value,
                frequency_penalty=float(self.llm_model.frequency_penalty),
                presence_penalty=float(self.llm_model.presence_penalty),
                max_tokens=int(self.llm_model.maximum_tokens),
                top_p=float(self.llm_model.top_p))

            choices = llm_response.choices
            first_choice = choices[0]

            choice_message = first_choice.message
            choice_message_content = choice_message.content
            final_response = choice_message_content

            tx = LLMTransaction.objects.create(
                organization=self.process.organization,
                model=self.llm_model,
                responsible_user=self.process.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(final_response),
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.BINEXUS
            )

            tx.save()

            logger.info(
                f"[_create_assignment] Created response (system) prompt LLM Transaction for Binexus Assignment Creation.")

        except Exception as e:
            final_response = f"""
                ---
                Unfortunately, I couldn't complete my assignment. I am sorry for my failure.
                According to the regulations, you MUST give me a zero (0) score as my fitness score.
                ---
            """
            logger.error(f"Error while creating assignment: {e}")

        return final_response

    def set_new_fitness_score(
        self,
        score
    ):
        self.fitness = score

    def get_chromosome(self):
        return self.chromosome
