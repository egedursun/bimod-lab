#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: constant_utils.py
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
#   For permission inquiries, please contact: admin@br6.in.
#


class AnalysisToolCallExecutionTypesNames:
    FILE_INTERPRETATION = "file_interpretation"
    IMAGE_INTERPRETATION = "image_interpretation"


class ToolCallDescriptorNames:
    EXECUTE_SQL_QUERY = 'SQL Query Execution'
    EXECUTE_NOSQL_QUERY = 'NoSQL Query Execution'
    EXECUTE_VECTOR_STORE_QUERY = 'Knowledge Base Query Execution'
    EXECUTE_CODE_BASE_QUERY = 'Code Base Query Execution'
    EXECUTE_INTRA_MEMORY_QUERY = 'Vector Chat History Query Execution'
    EXECUTE_SSH_SYSTEM_QUERY = 'File System Command Execution'
    EXECUTE_MEDIA_MANAGER_QUERY = 'Media Storage Query Execution'
    EXECUTE_BROWSING = 'Browsing'
    EXECUTE_HTTP_DELIVERY = 'URL File Uploader'
    EXECUTE_HTTP_RETRIEVAL = 'URL File Downloader'
    EXECUTE_INFER_WITH_ML = 'Prediction with ML Model'
    EXECUTE_ANALYZE_CODE = 'Code Interpreter'
    EXECUTE_CUSTOM_FUNCTION = 'Custom Function Executor'
    EXECUTE_CUSTOM_API = 'Custom API Executor'
    EXECUTE_CUSTOM_SCRIPT = 'Custom Script Content Retrieval'
    EXECUTE_GENERATE_IMAGE = 'Image Generation'
    EXECUTE_EDIT_IMAGE = 'Image Modification'
    EXECUTE_DREAM_IMAGE = 'Image Variation'
    EXECUTE_PROCESS_AUDIO = 'Audio Processing'
    EXECUTE_GENERATE_VIDEO = 'Video Generation'
    EXECUTE_REASONING_PROCESS = 'Reasoning'
    EXECUTE_EXPERT_NETWORK_QUERY = 'Expert Network Query Call'
    EXECUTE_ORCHESTRATION_WORKER_CONSULTANCY = 'Orchestration Worker Assistant Call'


IMAGE_GENERATION_AFFIRMATION_PROMPT = f"""
    **Important Note:**
    Always include the generated image's URL in your
    response's image_uris list or the equivalent.
"""

VISUALIZATION_TOOL_ERROR_LOG = ("This assistant is not authorized to do visualization tool operations. The assistant "
                                "must first be edited to allow image generation capabilities to be able to use "
                                "this tool.")

VISUALIZATION_TOOL_STANDARD_ERROR_LOG = f"Error occurred while working on visualization capability tool."
