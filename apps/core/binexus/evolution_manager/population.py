#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: population.py
#  Last Modified: 2024-10-22 03:15:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 03:15:08
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
from apps.core.binexus.evolution_manager import Individual, Chromosome
from apps.llm_core.models import LLMCore


class PopulationManager:
    def __init__(self, process: BinexusProcess, llm_model: LLMCore, population_size: int):
        self.process = process
        self.llm_model = llm_model
        self.population_size = population_size

        self.best_individual = None
        self.best_fitness = None
        self.average_fitness = None
        self.worst_individual = None
        self.worst_fitness = None

        self.total_generations = 0
        self.total_evaluations = 0
        self.total_mutations = 0
        self.total_crossovers = 0

    def get_population(self):
        return self.population

    def get_population_size(self):
        return self.population_size

    def get_best_individual(self):
        return self.best_individual

    def get_average_fitness(self):
        return self.average_fitness

    def build_population_with_size(self):
        print("Initializing First Population")
        print("---------process: generating first population: start-----------")
        generated_population = []
        for i in range(self.population_size):
            new_individual = Individual(
                process=self.process,
                chromosome=Chromosome.get_random_chromosome(custom_genes=self.process.additional_genes),
                llm_model=self.llm_model
            )
            generated_population.append(new_individual)
        print("- Population Initialized Successfully")
        print("---------process: generating first population: end-----------")
        return generated_population

    def build_hall_of_fame(self, population):
        best_fitness, worst_fitness, total_fitness = -1, 101, 0
        best_individual, worst_individual = None, None
        for individual in population:
            fitness = individual.get_fitness_score()
            if fitness > best_fitness:
                best_fitness = fitness
                best_individual = individual
            if fitness < worst_fitness:
                worst_fitness = fitness
                worst_individual = individual
            total_fitness += fitness

        print("Hall of Fame for the Generation")
        print("------------process: hall of fame creation: start-------------------")
        self.best_individual = best_individual
        self.best_fitness = best_fitness
        self.worst_individual = worst_individual
        self.worst_fitness = worst_fitness
        self.average_fitness = (total_fitness / self.population_size)
        print("- Best Individual - Fitness Score:", best_fitness)
        print("- Worst Individual - Fitness Score:", worst_fitness)
        print("- Average Fitness Score:", self.average_fitness)
        print("---------------process: hall of fame creation: end----------------")

    def replace_population(self, new_population):
        print("Replacing Population")
        print("---------process: replacing population: start-----------")
        self.population = []
        self.population = new_population
        print("- Population Replaced Successfully")
        print("---------process: replacing population: end-----------")

    @staticmethod
    def order_population_by_fitness_descending(population):
        order_population = sorted(population, key=lambda individual: individual.get_fitness_score(), reverse=True)
        return order_population
