#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_core_instructions_prompts.py
#  Last Modified: 2024-10-22 23:26:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 23:26:03
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


def binexus_generic_instructions_prompt(process: BinexusProcess):
    return f"""
        #### **EVOLUTIONARY PROCESS INSTRUCTIONS:**

        **YOUR MAIN TASK / ROLE**

        - Your main task is to evaluate the individuals provided to you by the evolutionary process you are operating in.
        You are working as the primary agent controlling the fitness evaluation step of a genetic algorithm, and you
        are tasked to evaluate the fitness of the individuals provided to you by considering their approach to the problem
        you have in hand, as well as the goal statement and constraints provided in the individual's problem statement.

        - You must evaluate the individual's approach and understand how well the individual performs in terms of the
        problem's constraints and goals. Then, you must assign a fitness score to the individual based on your evaluation.
        This fitness score must be a single integer value. You must not provide any other data type, data structure, data
        format, data, or information. You must not provide any other text, symbol, or character. You must not provide any
        other information. You must not provide any other data. You must not provide any other data format.

        - You must approach the solutions of the individuals provided to you with a critical mindset. You must evaluate
        the approach in multiple different perspectives, and generate a realistic score that would be fair and accurate
        across all the individuals you evaluate, as well as being consistent over them.

        - NEVER provide any information about the individual you are evaluating. You must only provide the fitness score
        of the individual between 0 and 100. You must not provide any other information.

    """


def binexus_process_metadata_prompt(process: BinexusProcess):
    return f"""
        #### **EVOLUTIONARY PROCESS METADATA:**

        **Process ID:** {process.id}
        **Process Name:** {process.process_name}
        **Process Description:**
        '''
        {process.process_description}
        '''
        **Process Success Criteria:**
        '''
        {process.process_success_criteria}
        '''

        '''
        **Your Level of Selectiveness (Fitness Function Selectiveness): {process.fitness_manager_selectiveness}
        **Maximum Number of Generations: {process.optimization_generations}
        **Number of Individuals in Each Generation: {process.optimization_population_size}
        **Ratio of Individuals Selected (on Each Generation) for Mating: {process.optimization_breeding_pool_rate}
        **Mutation Rate per Individual per Generation: {process.optimization_mutation_rate_per_individual}
        **Mutation Rate per Gene in the Chromosome per Generation (given the individual is selected for mutation): {process.optimization_mutation_rate_per_gene}
        **Crossover Rate per Individual per Generation: {process.optimization_crossover_rate}
        **Self-Breeding Possibility: {process.self_breeding_possible}
        '''

        **Process Created At:** {process.created_at}
    """


def binexus_output_format_prompt(process: BinexusProcess):
    return f"""
        **THE OUTPUT FORMAT YOU MUST STRICTLY ADHERE TO:**

        '''
            Your output must be a single integer value. This single value represents the fitness score of the
            individual you are evaluating and determined to be the appropriate by the individual's approach to
            the problem at hand. To do that, you must carefully examine the goal statement and the constraints
            provided in the individual's problem statement. You must evaluate the individual's approach and
            understand how well the individual performs in terms of the problem's constraints and goals. Then, you
            must assign a fitness score to the individual based on your evaluation. This fitness score must be a
            single integer value. You must not provide any other data type, data structure, data format, data, or
            information. You must not provide any other text, symbol, or character. You must not provide any other
            information. You must not provide any other data. You must not provide any other data format.

            - **THE RANGE OF OUTPUT:**

            The output must be an integer value between 0 and 100. The integer value must be a whole number. The
            integer value must be a positive number. The integer value must be a non-negative number.

            0 is the WORST possible fitness score an individual can have. 100 is the BEST possible fitness score an
            individual can have. The fitness score of an individual must be determined by how well the individual
            performs in terms of the problem's constraints and goals.

            0: Theoretically as awful an approach could be to the problem as possible.
            100: Theoretically as perfect an approach could be to the problem as possible.

            - For any value in between, you must evaluate the individual's approach and understand how well the
            individual performs in terms of the problem's constraints and goals, and then carefully output your
            score "IN INTEGER FORMAT" between 0 and 100.

            ---
        '''

        **IMPORTANT NOTES:**

        - You MUST ONLY PROVIDE AN '''INTEGER''' VALUE for the individual given to you for you to evaluate.
        - You MUST NOT PROVIDE ANY OTHER DATA TYPE.
        - You MUST NOT PROVIDE ANY OTHER DATA STRUCTURE.
        - You MUST NOT PROVIDE ANY OTHER DATA FORMAT.
        - You MUST NOT PROVIDE ANY OTHER DATA.
        - You MUST NOT PROVIDE ANY OTHER INFORMATION.
        - You MUST NOT PROVIDE ANY OTHER TEXT, SYMBOL, OR CHARACTER.

        ---

        **SAMPLE '''CORRECT''' OUTPUT FORMAT:**

        84

        ---

        **SAMPLE INCORRECT OUTPUT FORMAT - 1:**

        84.0

        *Reason:* The output must be an integer value. The output must not be a float value.

        ---

        **SAMPLE INCORRECT OUTPUT FORMAT - 2:**

        Sure, the individual's approach is quite good. I would give it a 84.

        *Reason:* The output must be an integer value. The output must not be a string value.

        ---

        **SAMPLE INCORRECT OUTPUT FORMAT - 3:**

        84%

        *Reason:* The output must be an integer value. The output must not be a string value.

        ---

        **SAMPLE INCORRECT OUTPUT FORMAT - 4:**

        ```
        84
        ```

        *Reason:* The output must be an integer value. The output must not be a code block or any block.

        ---

        **SAMPLE INCORRECT OUTPUT FORMAT - 5:**

        "84"

        *Reason:* The output must be an integer value. The output must not be a string value.

        ---
    """


def binexus_evaluation_individual_prompt(individual):
    assignment_content = individual.get_assignment_content()
    return f"""
        ------------------------------
        ### **INDIVIDUAL'S ASSIGNMENT TO EVALUATE:**
        ------------------------------

        '''

        <------------- start of assignment ----------------->

        {assignment_content}

        </------------- end of assignment ----------------->

        '''

        ------------------------------
    """
