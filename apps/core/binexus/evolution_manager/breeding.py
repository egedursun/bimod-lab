#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: breeding.py
#  Last Modified: 2024-10-22 03:25:18
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 03:25:19
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.binexus.models import BinexusProcess

from apps.core.binexus.evolution_manager import (
    PopulationManager,
    Individual
)

import random

from apps.llm_core.models import LLMCore


class BreedingManager:
    def __init__(
        self,
        process: BinexusProcess,
        llm_model: LLMCore,
        population_size: int,
        crossover_rate: float,
        elitism_selection_ratio: float,
        self_mating_possible: bool = False
    ):
        self.process = process
        self.llm_model = llm_model
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.elitism_selection_ratio = elitism_selection_ratio
        self.self_mating_possible = self_mating_possible

    def _determine_elites(
        self,
        population
    ):
        elites = []
        selection_amount = int(self.population_size * self.elitism_selection_ratio)

        PopulationManager.order_population_by_fitness_descending(
            population=population
        )

        for i in range(selection_amount):
            elites.append(population[i])

        return elites

    def _apply_crossing_over(
        self,
        population,
        elites
    ):
        new_population = []

        for i in range(self.population_size):

            if random.random() < self.crossover_rate:
                parent_1 = random.choice(elites)

                if self.self_mating_possible:
                    parent_2 = random.choice(elites)

                else:
                    while True:
                        parent_2 = random.choice(elites)

                        if parent_1 != parent_2:
                            break

                parent_1_chromosome = parent_1.get_chromosome()
                parent_2_chromosome = parent_2.get_chromosome()

                child_chromosome = {}

                for gene_name, gene_value in parent_1_chromosome.items():

                    if random.random() < 0.5:
                        child_chromosome[gene_name] = gene_value

                    else:
                        child_chromosome[gene_name] = parent_2_chromosome[gene_name]

                new_individual = Individual(
                    process=self.process,
                    chromosome=child_chromosome,
                    llm_model=self.llm_model
                )

                new_population.append(new_individual)

            else:
                new_population.append(population[i])

        return new_population

    def produce_new_generation(
        self,
        population
    ):

        elites = self._determine_elites(population)

        new_population = self._apply_crossing_over(
            population,
            elites
        )

        return new_population
