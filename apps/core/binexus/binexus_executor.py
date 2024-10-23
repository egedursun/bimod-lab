#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_executor.py
#  Last Modified: 2024-10-22 02:44:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 02:44:49
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

from django.core.files.base import ContentFile

from apps.binexus.models import BinexusProcess
from apps.core.binexus.evolution_manager.matrix import Matrix
from apps.core.binexus.utils import generate_random_chart_file_name

logger = logging.getLogger(__name__)


class BinexusExecutionManager:

    def __init__(self, binexus_process: BinexusProcess):
        self.binexus_process = binexus_process

    def execute_binexus(self):
        mx = Matrix(
            binexus_process=self.binexus_process, population_size=self.binexus_process.optimization_population_size,
            mutation_rate_per_individual=self.binexus_process.optimization_mutation_rate_per_individual,
            mutation_rate_per_gene=self.binexus_process.optimization_mutation_rate_per_gene,
            cross_over_rate=self.binexus_process.optimization_crossover_rate,
            elitism_selection_ratio=self.binexus_process.optimization_breeding_pool_rate,
            self_mating_possible=self.binexus_process.self_breeding_possible,
            maximum_epochs=self.binexus_process.optimization_generations
        )
        success, error = mx.execute_evolution(is_test=False)
        if error is not None:
            logger.error(f"Error occurred during execution: {error}")
            return False, error

        self.binexus_process.post_processing_history_average_fitness_per_epoch = mx.average_fitness_per_epoch
        self.binexus_process.post_processing_history_best_fitness_per_epoch = mx.best_fitness_per_epoch
        self.binexus_process.post_processing_history_worst_fitness_per_epoch = mx.worst_fitness_per_epoch
        self.binexus_process.post_processing_history_average_of_average_fitnesses = mx.average_of_average_fitnesses
        self.binexus_process.post_processing_history_average_of_best_fitnesses = mx.average_of_best_fitnesses
        self.binexus_process.post_processing_history_average_of_worst_fitnesses = mx.average_of_worst_fitnesses
        if mx.process_history_chart:
            chart_name = f"binexus_process_chart_{generate_random_chart_file_name()}.png"
            chart_content = ContentFile(mx.process_history_chart)
            self.binexus_process.post_processing_history_visual_chart.save(chart_name, chart_content, save=False)
        self.binexus_process.save()
        logger.info("Binexus process execution completed successfully.")

        return success, None

