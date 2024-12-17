#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-12-14 17:09:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 17:09:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from typing import Tuple


class SinapteraEstimatorConstants:
    class CostEstimator:
        ORIGINAL_COST = 1.0
        GENERATIVE_COST_MULTIPLIER = 1.0
        EVALUATIVE_COST_MULTIPLIER = 0.6
        IMPROVEMENT_COST_MULTIPLIER = 1.5

        @staticmethod
        def get_generative_model_cost():
            return (
                SinapteraEstimatorConstants.CostEstimator.ORIGINAL_COST *
                SinapteraEstimatorConstants.CostEstimator.GENERATIVE_COST_MULTIPLIER
            )

        @staticmethod
        def get_evaluative_model_cost():
            return (
                SinapteraEstimatorConstants.CostEstimator.ORIGINAL_COST *
                SinapteraEstimatorConstants.CostEstimator.EVALUATIVE_COST_MULTIPLIER
            )

        @staticmethod
        def get_improvement_model_cost():
            return (
                SinapteraEstimatorConstants.CostEstimator.ORIGINAL_COST *
                SinapteraEstimatorConstants.CostEstimator.IMPROVEMENT_COST_MULTIPLIER
            )

    class SpeedEstimator:
        BASE_MODEL_SPEED = 1.0

        GENERATIVE_MODEL_SPEED_MULTIPLIER = 1.0
        EVALUATIVE_MODEL_SPEED_MULTIPLIER = 0.2
        IMPROVEMENT_MODEL_SPEED_MULTIPLIER = 1.0

        @staticmethod
        def get_generative_model_speed():
            return (
                SinapteraEstimatorConstants.SpeedEstimator.BASE_MODEL_SPEED *
                SinapteraEstimatorConstants.SpeedEstimator.GENERATIVE_MODEL_SPEED_MULTIPLIER
            )

        @staticmethod
        def get_evaluative_model_speed():
            return (
                SinapteraEstimatorConstants.SpeedEstimator.BASE_MODEL_SPEED *
                SinapteraEstimatorConstants.SpeedEstimator.EVALUATIVE_MODEL_SPEED_MULTIPLIER
            )

        @staticmethod
        def get_improvement_model_speed():
            return (
                SinapteraEstimatorConstants.SpeedEstimator.BASE_MODEL_SPEED *
                SinapteraEstimatorConstants.SpeedEstimator.IMPROVEMENT_MODEL_SPEED_MULTIPLIER
            )

    class AccuracyEstimator:
        ORIGINAL_ACCURACY = 0.864

        @staticmethod
        def get_original_inaccuracy():
            return (
                1.0 - SinapteraEstimatorConstants.AccuracyEstimator.ORIGINAL_ACCURACY
            )


def estimate_sinaptera_cost_multiplier(N, M, D) -> Tuple[float, float]:
    c_gen = (
        SinapteraEstimatorConstants.CostEstimator.get_generative_model_cost()
    )

    c_eval = (
        SinapteraEstimatorConstants.CostEstimator.get_evaluative_model_cost()
    )

    c_imp = (
        SinapteraEstimatorConstants.CostEstimator.get_improvement_model_cost()
    )

    total_cost = 0.0

    total_cost += N * c_gen

    for d in range(1, D + 1):
        total_cost += (N - M) * c_eval
        total_cost += (M * N) * c_imp

    total_cost += M * (N - 1) * c_eval

    if M > 1:
        total_cost += (M - 1) * c_eval

    cost_ratio = round(total_cost / 1.0, 2)

    cost_ratio_percentage = round(cost_ratio * 100.0, 2)

    return cost_ratio, cost_ratio_percentage


def estimate_sinaptera_speed_percentage(N, M, D) -> Tuple[float, float]:
    t_gen = (
        SinapteraEstimatorConstants.SpeedEstimator.get_generative_model_speed()
    )

    t_eval = (
        SinapteraEstimatorConstants.SpeedEstimator.get_evaluative_model_speed()
    )

    t_imp = (
        SinapteraEstimatorConstants.SpeedEstimator.get_improvement_model_speed()
    )

    total_time = N * t_gen

    for d in range(1, D + 1):
        total_time += (N - M) * t_eval
        total_time += (M * N) * t_imp

    total_time += M * (N - 1) * t_eval

    if M > 1:
        total_time += (M - 1) * t_eval

    speed_factor = 1.0 / total_time

    speed_percentage = (1.0 / total_time) * 100.0

    return round(speed_factor, 2), round(speed_percentage, 2)


def estimate_sinaptera_accuracy(N, M, D) -> Tuple[float, float]:
    original_inaccuracy = SinapteraEstimatorConstants.AccuracyEstimator.get_original_inaccuracy()

    if D == 0:
        final_completions = N
    else:
        final_completions = M * N

    final_inaccuracy = original_inaccuracy ** final_completions

    improvement_factor = (1.00 - final_inaccuracy) - (1.00 - original_inaccuracy)
    improvement_factor_percentage = improvement_factor * 100.0

    return round(improvement_factor, 2), round(improvement_factor_percentage, 2)


############################################################################################
# TESTING
############################################################################################

if __name__ == "__main__":
    tN = 2
    tM = 1
    tD = 1

    cost_multiplier = estimate_sinaptera_cost_multiplier(
        N=tN,
        M=tM,
        D=tD
    )

    time_percentage = estimate_sinaptera_speed_percentage(
        N=tN,
        M=tM,
        D=tD
    )

    accuracy = estimate_sinaptera_accuracy(
        N=tN,
        M=tM,
        D=tD
    )

    print("Estimated Sinaptera Cost Multiplier: ", cost_multiplier)
    print("Estimated Sinaptera Speed Percentage: ", time_percentage)
    print("Estimated Improvement Factor: ", accuracy)
