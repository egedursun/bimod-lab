#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: matrix.py
#  Last Modified: 2024-10-22 03:31:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 03:31:37
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
import matplotlib

from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

from apps.binexus.models import BinexusProcess

from apps.core.binexus.evolution_manager import (
    PopulationManager,
    MutationManager,
    Individual
)

from apps.core.binexus.evolution_manager.breeding import BreedingManager
from apps.core.binexus.evolution_manager.fitness import FitnessEvaluationManager

from apps.core.binexus.utils import generate_random_chart_file_name

logger = logging.getLogger(__name__)


class Matrix:
    def __init__(
        self,
        binexus_process: BinexusProcess,
        population_size: int,
        mutation_rate_per_individual: float,
        mutation_rate_per_gene: float,
        cross_over_rate: float,
        elitism_selection_ratio: float,
        self_mating_possible: bool = False,
        maximum_epochs: int = 10
    ):
        self.binexus_process = binexus_process
        self._current_epoch = 0
        self.maximum_epochs = maximum_epochs

        self.population_size = population_size
        self.population_manager = PopulationManager(
            process=self.binexus_process,
            population_size=self.population_size,
            llm_model=binexus_process.llm_model
        )
        self.population = self.population_manager.build_population_with_size()

        self.fitness_manager = FitnessEvaluationManager(
            binexus_process=binexus_process,
            custom_genes=binexus_process.additional_genes
        )

        self.breeding_manager = BreedingManager(
            process=self.binexus_process,
            llm_model=binexus_process.llm_model,
            population_size=self.population_size,
            crossover_rate=cross_over_rate,
            elitism_selection_ratio=elitism_selection_ratio,
            self_mating_possible=self_mating_possible
        )
        self.mutation_manager = MutationManager(
            mutation_chance_per_individual=mutation_rate_per_individual,
            conditional_mutation_chance_per_gene=mutation_rate_per_gene
        )

        self.mutation_rate_per_individual = mutation_rate_per_individual
        self.mutation_rate_per_gene = mutation_rate_per_gene
        self.cross_over_rate = cross_over_rate
        self.elitism_selection_ratio = elitism_selection_ratio
        self.self_mating_possible = self_mating_possible

        # History
        self.average_fitness_per_epoch = []
        self.best_fitness_per_epoch = []
        self.worst_fitness_per_epoch = []
        self.average_of_average_fitnesses = None
        self.average_of_best_fitnesses = None
        self.average_of_worst_fitnesses = None
        self.process_history_chart = None
        self.latest_parents = None

    def execute_evolution(
        self,
        is_test=False
    ):
        try:
            latest_parents = self.population
            while self._current_epoch < self.maximum_epochs:
                latest_parents = self.iterate_epoch(
                    is_test=is_test
                )

                tx = LLMTransaction(
                    organization=self.binexus_process.organization,
                    model=self.binexus_process.llm_model,
                    responsible_user=self.binexus_process.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    llm_cost=InternalServiceCosts.Binexus.COST,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=LLMTransactionSourcesTypesNames.BINEXUS,
                    is_tool_cost=True
                )
                tx.save()
                logger.info(f"[execute_evolution] Created LLM TOOL cost Transaction for Binexus Evolution Process.")

            for individual in latest_parents:

                individual: Individual
                success = individual.ascend_to_elite()
                if success is False:
                    logger.error(f"Error occurred while ascending to elite for individual: {individual}")
                    continue

            logger.info("Evolution and ascending process completed successfully.")
            print("Evolution and ascending process completed successfully.")

            self.average_of_average_fitnesses = sum(self.average_fitness_per_epoch) / len(
                self.average_fitness_per_epoch)
            self.average_of_best_fitnesses = sum(self.best_fitness_per_epoch) / len(self.best_fitness_per_epoch)
            self.average_of_worst_fitnesses = sum(self.worst_fitness_per_epoch) / len(self.worst_fitness_per_epoch)

            if is_test is True:
                self.visualize()
            else:
                self.save_visual_records()

        except Exception as e:
            error = f"Error occurred during evolution execution: {e}"
            logger.error("Error occurred during evolution execution: %s", e)
            return False, error

        return True, None

    def iterate_epoch(
        self,
        is_test
    ):

        self._current_epoch += 1
        evaluated_population = self.fitness_manager.evaluate_and_record_population_fitness(
            population=self.population,
            is_test=is_test
        )

        self.population = evaluated_population
        self.population_manager.build_hall_of_fame(
            population=self.population
        )

        children = self.breeding_manager.produce_new_generation(
            population=self.population
        )

        mutated_children = self.mutation_manager.mutate_population(
            population=children
        )

        self.latest_parents = self.population
        self.population = mutated_children

        self.average_fitness_per_epoch.append(self.population_manager.average_fitness)
        self.best_fitness_per_epoch.append(self.population_manager.best_fitness)
        self.worst_fitness_per_epoch.append(self.population_manager.worst_fitness)
        return self.latest_parents

    def visualize(self):

        plt.plot(self.average_fitness_per_epoch, label='Average Fitness')
        plt.plot(self.best_fitness_per_epoch, label='Best Fitness')
        plt.plot(self.worst_fitness_per_epoch, label='Worst Fitness')
        plt.legend()
        plt.show()

    def save_visual_records(self):

        plt.style.use('dark_background')

        plt.title(
            'Evolutionary Optimization Process History',
            color='white'
        )
        plt.plot(
            self.average_fitness_per_epoch,
            label='Average Fitness per Generation',
            color='yellow'
        )
        plt.plot(
            self.best_fitness_per_epoch,
            label='Best Fitness per Generation',
            color='green'
        )
        plt.plot(
            self.worst_fitness_per_epoch,
            label='Worst Fitness per Generation',
            color='red'
        )

        plt.xlabel(
            'Generations',
            color='white'
        )
        plt.ylabel(
            'Fitness Level (Absolute)',
            color='white'
        )
        plt.tick_params(
            colors='white'
        )

        ax = plt.gca()
        ax.set_facecolor('#333333')
        plt.gcf().patch.set_facecolor('#1e1e1e')
        plt.grid(
            color='gray',
            linestyle='--'
        )
        legend = plt.legend()
        plt.setp(
            legend.get_texts(),
            color='white'
        )

        tmp_path = os.path.join(os.path.dirname(__file__), 'tmp')
        randomized_filename_component = generate_random_chart_file_name()
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        plt.savefig(os.path.join(tmp_path, f'process_optimization_chart_{randomized_filename_component}.png'))
        plt.close()

        try:
            with open(
                os.path.join(
                    tmp_path,
                    f'process_optimization_chart_{randomized_filename_component}.png'
                ),
                'rb'
            ) as f:
                self.process_history_chart = f.read()

        except Exception as e:
            logger.error(f"Error occurred while converting the image file into bytes: {e}")

        try:
            os.remove(
                os.path.join(
                    tmp_path,
                    f'process_optimization_chart_{randomized_filename_component}.png'
                )
            )
        except Exception as e:
            logger.error(f"Error occurred while deleting the image file from temporary folder: {e}")

    def flush(self):
        self._current_epoch = 0
        self.population = self.population_manager.build_population_with_size()
