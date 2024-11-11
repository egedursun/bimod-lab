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
    ("miscellaneous", "Miscellaneous")
]


class MLModelIntegrationCategoriesNames:
    COMPUTER_VISION = "computer_vision"
    GENERATIVE_AI = "generative_ai"
    GRAPH_MACHINE_LEARNING = "graph_machine_learning"
    NATURAL_LANGUAGE_PROCESSING = "natural_language_processing"
    MISCELLANEOUS = "miscellaneous"

    @staticmethod
    def as_list():
        return [
            MLModelIntegrationCategoriesNames.COMPUTER_VISION,
            MLModelIntegrationCategoriesNames.GENERATIVE_AI,
            MLModelIntegrationCategoriesNames.GRAPH_MACHINE_LEARNING,
            MLModelIntegrationCategoriesNames.NATURAL_LANGUAGE_PROCESSING,
            MLModelIntegrationCategoriesNames.MISCELLANEOUS
        ]


ML_MODEL_INTEGRATION_ADMIN_LIST = ["name", "model_category", "created_at", "updated_at"]
ML_MODEL_INTEGRATION_ADMIN_FILTER = ["model_category", "created_at", "updated_at"]
ML_MODEL_INTEGRATION_ADMIN_SEARCH = ["name", "model_category", "created_at", "updated_at"]
