#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: mutation.py
#  Last Modified: 2024-10-22 03:11:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 03:11:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import random

from apps.core.binexus.evolution_manager import Individual, Chromosome
from apps.core.binexus.evolution_manager.population import PopulationManager


class MutationManager:
    def __init__(
        self,
        mutation_chance_per_individual: float,
        conditional_mutation_chance_per_gene: float
    ):

        self.mutation_chance_per_individual = mutation_chance_per_individual
        self.mutation_chance_per_gene = conditional_mutation_chance_per_gene

    def _mutate_individual(
        self,
        individual: Individual
    ) -> Individual:

        mutated_chromosome = {}
        for gene_name, gene_value in individual.get_chromosome().items():
            if random.random() < self.mutation_chance_per_gene:
                mutated_gene_value = Chromosome.give_random_value_of_gene(gene_name)
                mutated_chromosome[gene_name] = mutated_gene_value
            else:
                mutated_chromosome[gene_name] = gene_value
        individual.chromosome = mutated_chromosome

        return individual

    def mutate_population(
        self,
        population: PopulationManager
    ) -> list:

        mutated_population = []
        for i, individual in enumerate(population):
            if random.random() < self.mutation_chance_per_individual:
                mutated_individual = self._mutate_individual(individual)
                mutated_population.append(mutated_individual)
            else:
                mutated_population.append(individual)

        return mutated_population
