#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_ml_models_data_source_prompt.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from apps.assistants.models import Assistant

from apps.datasource_ml_models.models import (
    DataSourceMLModelConnection
)


def build_ml_models_data_source_prompt(assistant: Assistant):
    ml_model_data_sources = DataSourceMLModelConnection.objects.filter(
        assistant=assistant
    )

    response_prompt = """
            ### **ML MODELS RESOURCE CONNECTIONS:**

            '''
            """

    for i, ml_model_data_source in enumerate(ml_model_data_sources):
        response_prompt += f"""
                [ML Data Source ID: {ml_model_data_source.id}]
                    Source Name: {ml_model_data_source.name}
                    Source Description: {ml_model_data_source.description or "N/A"}
                    Source Category: {ml_model_data_source.model_object_category}

                    #### *Names and Descriptions of the ML Models in this Storage:*
                """

        ml_model_items = ml_model_data_source.items.all()

        for j, model_item in enumerate(ml_model_items):
            response_prompt += f"""
                    - [ML Model Item ID: {model_item.id}]
                        Model Name: {model_item.ml_model_name}
                        Model Description: {model_item.description or "N/A"}
                        Model Size: {model_item.ml_model_size or "N/A"}
                        File Path: {model_item.full_file_path}
                        Created At: {model_item.created_at}
                """

    response_prompt += """
            '''

            ---

            #### **VERY IMPORTANT NOTE ABOUT THE ''URL DOWNLOADER TOOL''**
            - When the user sends you an image content through CHAT, this content is automatically processed and
            saved, so you DON'T NEED to use your 'URL RETRIEVER' tool to download the content, as it is already saved
            in your storage.

            #### **NOTE**: These are the ML Model connections you have. You can use these to retrieve info about the
            ML Models, ask questions about them, and retrieve inference and predictions.

            #### **IMPORTANT NOTE ABOUT 'ML MODELS' RESOURCE CONNECTIONS:**
            - This is a direct connection to the ML Models. You can use these to retrieve info about the ML Models,
            ask queries and questions, and retrieve inference & predictions.
            - You can also request chart generations and other types of visualizations to provide an accurate and
            detailed response.

            #### **HOW YOUR QUERIES ARE PROCESSED:**
            - Your queries with the file paths you give will be send to a distinct agent which will process the
            queries and provide you the results. The results will be displayed in the response of the agent, along
            with the URIs of the generated files, if any.

            ---
            """

    return response_prompt


def build_semantor_ml_models_data_source_prompt(temporary_sources: dict):
    ml_model_data_sources = temporary_sources.get("data_sources").get("ml_storages")

    response_prompt = """
            ### **ML MODELS RESOURCE CONNECTIONS:**

            '''
            """

    for i, ml_model_data_source in enumerate(ml_model_data_sources):
        response_prompt += f"""
                [ML Data Source ID: {ml_model_data_source.id}]
                    Source Name: {ml_model_data_source.name}
                    Source Description: {ml_model_data_source.description or "N/A"}
                    Source Category: {ml_model_data_source.model_object_category}

                    #### *Names and Descriptions of the ML Models in this Storage:*
                """

        ml_model_items = ml_model_data_source.items.all()

        for j, model_item in enumerate(ml_model_items):
            response_prompt += f"""
                    - [ML Model Item ID: {model_item.id}]
                        Model Name: {model_item.ml_model_name}
                        Model Description: {model_item.description or "N/A"}
                        Model Size: {model_item.ml_model_size or "N/A"}
                        File Path: {model_item.full_file_path}
                        Created At: {model_item.created_at}
                """

    response_prompt += """
            '''

            ---

            #### **VERY IMPORTANT NOTE ABOUT THE ''URL DOWNLOADER TOOL''**
            - When the user sends you an image content through CHAT, this content is automatically processed and
            saved, so you DON'T NEED to use your 'URL RETRIEVER' tool to download the content, as it is already saved
            in your storage.

            #### **NOTE**: These are the ML Model connections you have. You can use these to retrieve info about the
            ML Models, ask questions about them, and retrieve inference and predictions.

            #### **IMPORTANT NOTE ABOUT 'ML MODELS' RESOURCE CONNECTIONS:**
            - This is a direct connection to the ML Models. You can use these to retrieve info about the ML Models,
            ask queries and questions, and retrieve inference & predictions.
            - You can also request chart generations and other types of visualizations to provide an accurate and
            detailed response.

            #### **HOW YOUR QUERIES ARE PROCESSED:**
            - Your queries with the file paths you give will be send to a distinct agent which will process the
            queries and provide you the results. The results will be displayed in the response of the agent, along
            with the URIs of the generated files, if any.

            ---
            """

    return response_prompt


def build_lean_ml_models_data_source_prompt():
    response_prompt = """
            ### **ML MODELS RESOURCE CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            ---

            #### **VERY IMPORTANT NOTE ABOUT THE ''URL DOWNLOADER TOOL''**
            - When the user sends you an image content through CHAT, this content is automatically processed and
            saved, so you DON'T NEED to use your 'URL RETRIEVER' tool to download the content, as it is already saved
            in your storage.

            #### **NOTE**: These are the ML Model connections you have. You can use these to retrieve info about the
            ML Models, ask questions about them, and retrieve inference and predictions.

            #### **IMPORTANT NOTE ABOUT 'ML MODELS' RESOURCE CONNECTIONS:**
            - This is a direct connection to the ML Models. You can use these to retrieve info about the ML Models,
            ask queries and questions, and retrieve inference & predictions.
            - You can also request chart generations and other types of visualizations to provide an accurate and
            detailed response.

            #### **HOW YOUR QUERIES ARE PROCESSED:**
            - Your queries with the file paths you give will be send to a distinct agent which will process the
            queries and provide you the results. The results will be displayed in the response of the agent, along
            with the URIs of the generated files, if any.

            ---

            """
    return response_prompt
