#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: fitness.py
#  Last Modified: 2024-10-22 03:24:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 03:24:58
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

from apps.binexus.models import BinexusProcess

from apps.core.binexus.evolution_manager import (
    PopulationManager,
    Chromosome,
    Individual
)

from apps.core.binexus.prompt_builders import (
    build_binexus_fitness_evaluation_prompt
)

from apps.core.generative_ai.gpt_openai_manager import (
    OpenAIGPTClientManager
)

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

logger = logging.getLogger(__name__)


class FitnessEvaluationManager:
    def __init__(
        self,
        binexus_process: BinexusProcess,
        custom_genes: dict = None
    ):
        self.process = binexus_process
        self.custom_genes = {} if (custom_genes is None) else custom_genes
        self.llm_model = self.process.llm_model

        self.c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.llm_model
        )

    def _consult_ai(
        self,
        individual: Individual
    ):
        system_prompt = build_binexus_fitness_evaluation_prompt(
            process=self.process,
            individual=individual
        )

        structured_messages = [
            {
                "role": "system",
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

        logger.info(f"[_consult_ai] Created system prompt LLM Transaction for Binexus Fitness Evaluation.")

        temperature_of_evaluation_agent = (1.0 - self.process.fitness_manager_selectiveness)

        llm_response = self.c.chat.completions.create(
            model=self.llm_model.model_name,
            messages=structured_messages,
            temperature=temperature_of_evaluation_agent,
            frequency_penalty=float(self.llm_model.frequency_penalty),
            presence_penalty=float(self.llm_model.presence_penalty),
            max_tokens=int(self.llm_model.maximum_tokens),
            top_p=float(self.llm_model.top_p)
        )

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

        logger.info(f"[_consult_ai] Created response (system) prompt LLM Transaction for Binexus Fitness Evaluation.")

        try:
            final_response = int(final_response)

        except Exception as e:

            logger.error(f"The evaluation agent returned a non-integer response: {final_response}")
            final_response = 0

        return final_response

    def _evaluate_and_record_individual_fitness(
        self,
        individual,
        is_test
    ):
        calculated_fitness_score = 0

        if is_test is True:

            for gene_name, gene_value in individual.get_chromosome().items():

                if Chromosome.get_index_of_gene_value(
                    gene_name=gene_name,
                    gene_value=gene_value,
                    custom_genes=self.custom_genes
                ) == 0:
                    calculated_fitness_score += 1

        else:
            fitness_score = self._consult_ai(
                individual=individual
            )

            calculated_fitness_score = fitness_score

        individual.set_new_fitness_score(calculated_fitness_score)

    def evaluate_and_record_population_fitness(
        self,
        population,
        is_test
    ):

        for i, individual in enumerate(population):
            self._evaluate_and_record_individual_fitness(
                individual,
                is_test=is_test
            )

        order_population_by_fitness_descending = PopulationManager.order_population_by_fitness_descending(
            population
        )

        return order_population_by_fitness_descending
