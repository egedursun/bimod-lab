#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

class AnalysisToolCallExecutionTypesNames:
    FILE_INTERPRETATION = "file_interpretation"
    IMAGE_INTERPRETATION = "image_interpretation"


class ToolCallDescriptorNames:
    EXECUTE_SQL_QUERY = 'SQL Query Execution'
    EXECUTE_SQL_DATABASE_SCHEMA_SEARCH = 'SQL Database Schema Search'
    EXECUTE_NOSQL_QUERY = 'NoSQL Query Execution'
    EXECUTE_NOSQL_DATABASE_SCHEMA_SEARCH = 'NoSQL Database Schema Search'
    EXECUTE_VECTOR_STORE_QUERY = 'Knowledge Base Query Execution'
    EXECUTE_CODE_BASE_QUERY = 'Code Base Query Execution'
    EXECUTE_INTRA_MEMORY_QUERY = 'Vector Chat History Query Execution'
    EXECUTE_SSH_SYSTEM_QUERY = 'File System Command Execution'
    EXECUTE_SSH_SYSTEM_DIRECTORY_SCHEMA_SEARCH = 'File System Directory Schema Search'
    EXECUTE_MEDIA_ITEM_SEARCH_QUERY = 'Media Item Search Query Execution'
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
    EXECUTE_SMART_CONTRACT_FUNCTION_CALL = 'Smart Contract Function Call'
    EXECUTE_METAKANBAN_ACTION = 'Meta Kanban Command Execution'
    EXECUTE_SEMANTOR_SEARCH_QUERY = 'Semantor Search Query Execution'
    EXECUTE_SEMANTOR_CONSULTATION_QUERY = 'Semantor Consultation Query Execution'
    EXECUTE_DASHBOARD_STATISTICS_QUERY = 'Dashboard Statistics Query Execution'
    EXECUTE_HADRON_PRIME_NODE_QUERY = 'Hadron Prime Node Query Execution'
    EXECUTE_METAKANBAN_QUERY = 'MetaKanban Query Execution'
    EXECUTE_METATEMPO_QUERY = 'MetaTempo Query Execution'
    EXECUTE_ORCHESTRATION_TRIGGER = 'Orchestration Trigger'
    EXECUTE_SCHEDULED_JOB_LOGS_QUERY = 'Scheduled Job Logs Query Execution'
    EXECUTE_TRIGGERED_JOB_LOGS_QUERY = 'Triggered Job Logs Query Execution'
    EXECUTE_SMART_CONTRACT_GENERATION_QUERY = 'Smart Contract Generation Query'

    #####

    EXECUTE_VOIDFORGER_OLD_MESSAGE_SEARCH_QUERY = 'VoidForger Old Message Search Query Execution'
    EXECUTE_VOIDFORGER_ACTION_HISTORY_LOG_SEARCH_QUERY = 'VoidForger Action History Log Search Query Execution'
    EXECUTE_VOIDFORGER_AUTO_EXECUTION_LOG_SEARCH_QUERY = 'VoidForger Auto Execution Log Search Query Execution'
    EXECUTE_VOIDFORGER_LEANMOD_ORACLE_SEARCH_QUERY = 'VoidForger LeanMod Oracle Search Query Execution'
    EXECUTE_VOIDFORGER_LEANMOD_ORACLE_COMMAND_ORDER = 'VoidForger LeanMod Oracle Command Order Execution'


IMAGE_GENERATION_AFFIRMATION_PROMPT = f"""
    **Important Note:**
    Always include the generated image's URL in your
    response's image_uris list or the equivalent.
"""

VISUALIZATION_TOOL_ERROR_LOG = ("This assistant is not authorized to do visualization tool operations. The assistant "
                                "must first be edited to allow image generation capabilities to be able to use "
                                "this tool.")

VISUALIZATION_TOOL_STANDARD_ERROR_LOG = f"Error occurred while working on visualization capability tool."


class VoidForgerModesNames:
    AUTOMATED = "AUTOMATED"
    MANUAL = "MANUAL"
    CHAT = "CHAT"

    @staticmethod
    def as_list():
        return [
            VoidForgerModesNames.AUTOMATED,
            VoidForgerModesNames.MANUAL,
            VoidForgerModesNames.CHAT
        ]
