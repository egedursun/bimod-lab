#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: predict_with_ml_model_execution_handler.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: predict_with_ml_model_execution_handler.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.ml_models.ml_model_executor import MLModelExecutor
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.multimodal_chat.models import MultimodalChat


def execute_predict_ml_model(connection_id, chat_id, model_url, input_data_paths, query, without_chat=False):
    connection = DataSourceMLModelConnection.objects.get(id=connection_id)
    chat = None
    if without_chat is False:
        chat = MultimodalChat.objects.get(id=chat_id)

    try:
        executor = MLModelExecutor(connection=connection, chat=chat)
        print(f"[predict_with_ml_model_execution_handler.execute_predict_ml_model] Executing the ML model prediction "
              f"with the model URL: {model_url}.")
        response = executor.execute_predict_with_ml_model(model_url=model_url, file_urls=input_data_paths,
                                                          input_data=query)
        file_uris = response.get("file_uris")
        image_uris = response.get("image_uris")
    except Exception as e:
        error = (f"[predict_with_ml_model_execution_handler.execute_predict_ml_model] Error occurred while executing "
                 f"the ML model prediction: {str(e)}")
        return error
    print(f"[predict_with_ml_model_execution_handler.execute_predict_ml_model] ML model prediction executed "
          f"successfully.")
    return response, file_uris, image_uris
