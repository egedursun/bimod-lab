#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_infer_with_ml.py
#  Last Modified: 2024-10-05 02:31:01
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
import logging

from apps.core.ml_models.ml_model_executor import MLModelExecutor
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.multimodal_chat.models import MultimodalChat

logger = logging.getLogger(__name__)


def run_predict_with_ml(
    c_id,
    chat_id,
    model_item_url,
    input_data_uris,
    inference_query,
    no_chat=False
):
    conn = DataSourceMLModelConnection.objects.get(
        id=c_id
    )

    chat = None

    if no_chat is False:
        chat = MultimodalChat.objects.get(
            id=chat_id
        )

    try:
        xc = MLModelExecutor(
            connection=conn,
            chat=chat
        )

        output = xc.execute_predict_with_ml_model(
            model_url=model_item_url,
            file_urls=input_data_uris,
            input_data=inference_query
        )

        f_uris = output.get("file_uris")
        img_uris = output.get("image_uris")
        logger.info(f"ML model prediction output: {output}")

    except Exception as e:
        logger.error(f"Error occurred while executing the ML model prediction: {e}")
        error = f"Error occurred while executing the ML model prediction: {str(e)}"
        return error

    return output, f_uris, img_uris
