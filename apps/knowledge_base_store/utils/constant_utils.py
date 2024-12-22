#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-12-21 19:10:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-21 19:10:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


KNOWLEDGE_BASE_CATEGORIES = [
    ("software_and_it", "Software and IT"),
    ("legal_and_law", "Legal and Law"),
    ("healthcare_and_medicine", "Healthcare and Medicine"),
    ("finance_and_business", "Finance and Business"),
    ("education_and_training", "Education and Training"),

    ("science_and_engineering", "Science and Engineering"),
    ("history_and_culture", "History and Culture"),
    ("sports_and_entertainment", "Sports and Entertainment"),
    ("military_and_defense", "Military and Defense"),
    ("transport_and_logistics", "Transport and Logistics"),

    ("agriculture_and_food", "Agriculture and Food"),
    ("media_and_communication", "Media and Communication"),
    ("space_and_astronomy", "Space and Astronomy"),
    ("ethics_and_philosophy", "Ethics and Philosophy"),
    ('miscellaneous', 'Miscellaneous')
]


class KnowledgeBaseIntegrationCategoriesNames:
    SOFTWARE_AND_IT = "software_and_it"
    LEGAL_AND_LAW = "legal_and_law"
    HEALTHCARE_AND_MEDICINE = "healthcare_and_medicine"
    FINANCE_AND_BUSINESS = "finance_and_business"
    EDUCATION_AND_TRAINING = "education_and_training"

    SCIENCE_AND_ENGINEERING = "science_and_engineering"
    HISTORY_AND_CULTURE = "history_and_culture"
    SPORTS_AND_ENTERTAINMENT = "sports_and_entertainment"
    MILITARY_AND_DEFENSE = "military_and_defense"
    TRANSPORT_AND_LOGISTICS = "transport_and_logistics"

    AGRICULTURE_AND_FOOD = "agriculture_and_food"
    MEDIA_AND_COMMUNICATION = "media_and_communication"
    SPACE_AND_ASTRONOMY = "space_and_astronomy"
    ETHICS_AND_PHILOSOPHY = "ethics_and_philosophy"
    MISCELLANEOUS = "miscellaneous"

    @staticmethod
    def as_list():
        return [
            KnowledgeBaseIntegrationCategoriesNames.SOFTWARE_AND_IT,
            KnowledgeBaseIntegrationCategoriesNames.LEGAL_AND_LAW,
            KnowledgeBaseIntegrationCategoriesNames.HEALTHCARE_AND_MEDICINE,
            KnowledgeBaseIntegrationCategoriesNames.FINANCE_AND_BUSINESS,
            KnowledgeBaseIntegrationCategoriesNames.EDUCATION_AND_TRAINING,

            KnowledgeBaseIntegrationCategoriesNames.SCIENCE_AND_ENGINEERING,
            KnowledgeBaseIntegrationCategoriesNames.HISTORY_AND_CULTURE,
            KnowledgeBaseIntegrationCategoriesNames.SPORTS_AND_ENTERTAINMENT,
            KnowledgeBaseIntegrationCategoriesNames.MILITARY_AND_DEFENSE,
            KnowledgeBaseIntegrationCategoriesNames.TRANSPORT_AND_LOGISTICS,

            KnowledgeBaseIntegrationCategoriesNames.AGRICULTURE_AND_FOOD,
            KnowledgeBaseIntegrationCategoriesNames.MEDIA_AND_COMMUNICATION,
            KnowledgeBaseIntegrationCategoriesNames.SPACE_AND_ASTRONOMY,
            KnowledgeBaseIntegrationCategoriesNames.ETHICS_AND_PHILOSOPHY,
            KnowledgeBaseIntegrationCategoriesNames.MISCELLANEOUS,
        ]


KNOWLEDGE_BASE_INTEGRATION_ADMIN_LIST = [
    "name",
    "knowledge_base_category",
    "created_at",
    "updated_at"
]
KNOWLEDGE_BASE_INTEGRATION_ADMIN_FILTER = [
    "knowledge_base_category",
    "created_at",
    "updated_at"
]
KNOWLEDGE_BASE_INTEGRATION_ADMIN_SEARCH = [
    "name",
    "knowledge_base_category",
    "created_at",
    "updated_at"
]
