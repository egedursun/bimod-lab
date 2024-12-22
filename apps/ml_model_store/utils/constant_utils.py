#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-11-08 14:34:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-08 14:34:57
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


MODEL_CATEGORIES = [
    ("computer_vision", "Computer Vision"),
    ("generative_ai", "Generative AI"),
    ("graph_machine_learning", "Graph Machine Learning"),
    ("natural_language_processing", "Natural Language Processing"),
    ("time_series_analysis", "Time Series Analysis"),

    ("reinforcement_learning", "Reinforcement Learning"),
    ("audio_processing", "Audio Processing"),
    ("recommendation_systems", "Recommendation Systems"),
    ("tabular_data_learning", "Tabular Data Learning"),
    ("3d_data_processing", "3D Data Processing"),

    ("robotics_and_control", "Robotics and Control"),
    ("multimodal_learning", "Multimodal Learning"),
    ("biomedical_applications", "Biomedical Applications"),
    ("anomaly_detection", "Anomaly Detection"),
    ("miscellaneous", "Miscellaneous"),
]


class MLModelIntegrationCategoriesNames:
    COMPUTER_VISION = "computer_vision"
    GENERATIVE_AI = "generative_ai"
    GRAPH_MACHINE_LEARNING = "graph_machine_learning"
    NATURAL_LANGUAGE_PROCESSING = "natural_language_processing"
    TIME_SERIES_ANALYSIS = "time_series_analysis"

    REINFORCEMENT_LEARNING = "reinforcement_learning"
    AUDIO_PROCESSING = "audio_processing"
    RECOMMENDATION_SYSTEMS = "recommendation_systems"
    TABULAR_DATA_LEARNING = "tabular_data_learning"
    THREE_D_DATA_PROCESSING = "3d_data_processing"

    ROBOTICS_AND_CONTROL = "robotics_and_control"
    MULTIMODAL_LEARNING = "multimodal_learning"
    BIOMEDICAL_APPLICATIONS = "biomedical_applications"
    ANOMALY_DETECTION = "anomaly_detection"
    MISCELLANEOUS = "miscellaneous"

    @staticmethod
    def as_list():
        return [
            MLModelIntegrationCategoriesNames.COMPUTER_VISION,
            MLModelIntegrationCategoriesNames.GENERATIVE_AI,
            MLModelIntegrationCategoriesNames.GRAPH_MACHINE_LEARNING,
            MLModelIntegrationCategoriesNames.NATURAL_LANGUAGE_PROCESSING,
            MLModelIntegrationCategoriesNames.TIME_SERIES_ANALYSIS,

            MLModelIntegrationCategoriesNames.REINFORCEMENT_LEARNING,
            MLModelIntegrationCategoriesNames.AUDIO_PROCESSING,
            MLModelIntegrationCategoriesNames.RECOMMENDATION_SYSTEMS,
            MLModelIntegrationCategoriesNames.TABULAR_DATA_LEARNING,
            MLModelIntegrationCategoriesNames.THREE_D_DATA_PROCESSING,

            MLModelIntegrationCategoriesNames.ROBOTICS_AND_CONTROL,
            MLModelIntegrationCategoriesNames.MULTIMODAL_LEARNING,
            MLModelIntegrationCategoriesNames.BIOMEDICAL_APPLICATIONS,
            MLModelIntegrationCategoriesNames.ANOMALY_DETECTION,
            MLModelIntegrationCategoriesNames.MISCELLANEOUS,
        ]


ML_MODEL_INTEGRATION_ADMIN_LIST = [
    "name",
    "model_category",
    "created_at",
    "updated_at"
]
ML_MODEL_INTEGRATION_ADMIN_FILTER = [
    "model_category",
    "created_at",
    "updated_at"
]
ML_MODEL_INTEGRATION_ADMIN_SEARCH = [
    "name",
    "model_category",
    "created_at",
    "updated_at"
]
