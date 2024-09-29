#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: constant_utils.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:15:15
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

class ExecutionTypesNames:
    FILE_INTERPRETATION = "file_interpretation"
    IMAGE_INTERPRETATION = "image_interpretation"


class ToolTypeNames:
    ##############################
    SQL_QUERY_EXECUTION = 'SQL Query Execution'
    NOSQL_QUERY_EXECUTION = 'NoSQL Query Execution'
    KNOWLEDGE_BASE_QUERY_EXECUTION = 'Knowledge Base Query Execution'
    CODE_BASE_QUERY_EXECUTION = 'Code Base Query Execution'
    VECTOR_CHAT_HISTORY_QUERY_EXECUTION = 'Vector Chat History Query Execution'
    FILE_SYSTEM_COMMAND_EXECUTION = 'File System Command Execution'
    MEDIA_STORAGE_QUERY_EXECUTION = 'Media Storage Query Execution'
    BROWSING = 'Browsing'
    URL_FILE_UPLOADER = 'URL File Uploader'
    URL_FILE_DOWNLOADER = 'URL File Downloader'
    PREDICTION_WITH_ML_MODEL = 'Prediction with ML Model'
    CODE_INTERPRETER = 'Code Interpreter'
    CUSTOM_FUNCTION_EXECUTOR = 'Custom Function Executor'
    CUSTOM_API_EXECUTOR = 'Custom API Executor'
    CUSTOM_SCRIPT_CONTENT_RETRIEVAL = 'Custom Script Content Retrieval'
    IMAGE_GENERATION = 'Image Generation'
    IMAGE_MODIFICATION = 'Image Modification'
    IMAGE_VARIATION = 'Image Variation'
    AUDIO_PROCESSING = 'Audio Processing'
    ##############################
    EXPERT_NETWORK_QUERY_CALL = 'Expert Network Query Call'
    ##############################
    ORCHESTRATION_WORKER_ASSISTANT_CALL = 'Orchestration Worker Assistant Call'
    ##############################
