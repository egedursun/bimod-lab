from django.contrib.auth.models import User

from apps.assistants.models import Assistant
from apps.datasource_ml_models.models import DataSourceMLModelConnection


def build_ml_models_datasource_prompt(assistant: Assistant, user: User):
    response_prompt = ""
    # Gather the ML Model datasource connections of the assistant
    ml_model_datasources = DataSourceMLModelConnection.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
            **ML MODELS RESOURCE CONNECTIONS:**

            '''
            """

    for i, ml_model_datasource in enumerate(ml_model_datasources):
        response_prompt += f"""
                [ML Model Datasource ID: {ml_model_datasource.id}]
                    ML Model Name: {ml_model_datasource.name}
                    ML Model Description: {ml_model_datasource.description}
                    Ml Model Object Category: {ml_model_datasource.model_object_category}

                    *Names and Descriptions of the ML Models within this Connection:*
                """

        ml_model_items = ml_model_datasource.items.all()
        for j, model_item in enumerate(ml_model_items):
            response_prompt += f"""
                    - [ML Model Item ID: {model_item.id}]
                        ML Model Name: {model_item.ml_model_name}
                        ML Model Description: {model_item.description}
                        ML Model Size: {model_item.ml_model_size}
                        Full File Path: {model_item.full_file_path}
                        Created At: {model_item.created_at}
                """

    response_prompt += """
            -------

            '''

            **VERY IMPORTANT NOTE ABOUT THE ''URL DOWNLOADER TOOL''**
            - When the user sends you an image content through CHAT, this content is automatically processed and
            saved, so you DON'T NEED to use your 'URL RETRIEVER' tool to download the image content, since it is
            already saved in your storage.

            **NOTE**: These are the ML Model datasource connections you have. You can use these connections
            to retrieve information about the ML Models, ask queries and questions about them, and retrieve
            predictions from them.

            **VERY IMPORTANT NOTE ABOUT 'ML MODELS' RESOURCE CONNECTIONS:**
            - This is a direct connection to the ML Models you have. You can use these connections to retrieve
            information about the ML Models, ask queries and questions about them, and retrieve predictions from them.
            - You can also request chart generations and other types of data visualizations to provide a more
            accurate and detailed response to your queries.

            **HOW YOUR QUERIES ARE BEING PROCESSED:**
            - Your queries along with the file paths you have given will be send to a distinct GPT assistant which
            will process the queries and provide you with the results. The results will be displayed in the
            response of the assistant, along with the URIs of the generated files, if any.

            -------
            """

    return response_prompt
