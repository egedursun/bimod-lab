#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

MINUTES = 60
HOURS = 60 * MINUTES

DEFAULT_DASHBOARD_DAYS_BACK = 1


class TransactionSourcesNames:
    APP = "app"
    API = "api"
    GENERATION = "generation"
    SQL_READ = "sql-read"
    SQL_WRITE = "sql-write"
    STORE_MEMORY = "store-memory"
    INTERPRET_CODE = "interpret-code"
    DOWNLOAD_FILE = "download-file"
    FILE_SYSTEM_COMMANDS = "file-system-commands"
    KNOWLEDGE_BASE_SEARCH = "knowledge-base-search"
    RETRIEVE_MEMORY = "retrieve-memory"
    CODE_REPOSITORY_SEARCH = "code-repository-search"
    ML_MODEL_PREDICTION = "ml-model-prediction"
    BROWSING = "browsing"
    INTERNAL_FUNCTION_EXECUTION = "internal-function-execution"
    EXTERNAL_FUNCTION_EXECUTION = "external-function-execution"
    INTERNAL_API_EXECUTION = "internal-api-execution"
    EXTERNAL_API_EXECUTION = "external-api-execution"
    INTERNAL_SCRIPT_RETRIEVAL = "internal-script-retrieval"
    EXTERNAL_SCRIPT_RETRIEVAL = "external-script-retrieval"
    INTERPRET_FILE = "interpret-file"
    INTERPRET_IMAGE = "interpret-image"
    SCHEDULED_JOB_EXECUTION = "scheduled-job-execution"
    TRIGGER_JOB_EXECUTION = "trigger-job-execution"
    GENERATE_IMAGE = "generate-image"
    MODIFY_IMAGE = "modify-image"
    VARIATE_IMAGE = "variate-image"
    AUDIO_PROCESSING_STT = "audio-processing-stt"
    AUDIO_PROCESSING_TTS = "audio-processing-tts"

    @staticmethod
    def as_list():
        return [
            TransactionSourcesNames.APP,
            TransactionSourcesNames.API,
            TransactionSourcesNames.GENERATION,
            TransactionSourcesNames.SQL_READ,
            TransactionSourcesNames.SQL_WRITE,
            TransactionSourcesNames.STORE_MEMORY,
            TransactionSourcesNames.INTERPRET_CODE,
            TransactionSourcesNames.DOWNLOAD_FILE,
            TransactionSourcesNames.FILE_SYSTEM_COMMANDS,
            TransactionSourcesNames.KNOWLEDGE_BASE_SEARCH,
            TransactionSourcesNames.RETRIEVE_MEMORY,
            TransactionSourcesNames.CODE_REPOSITORY_SEARCH,
            TransactionSourcesNames.ML_MODEL_PREDICTION,
            TransactionSourcesNames.BROWSING,
            TransactionSourcesNames.INTERNAL_FUNCTION_EXECUTION,
            TransactionSourcesNames.EXTERNAL_FUNCTION_EXECUTION,
            TransactionSourcesNames.INTERNAL_API_EXECUTION,
            TransactionSourcesNames.EXTERNAL_API_EXECUTION,
            TransactionSourcesNames.INTERNAL_SCRIPT_RETRIEVAL,
            TransactionSourcesNames.EXTERNAL_SCRIPT_RETRIEVAL,
            TransactionSourcesNames.INTERPRET_FILE,
            TransactionSourcesNames.INTERPRET_IMAGE,
            TransactionSourcesNames.SCHEDULED_JOB_EXECUTION,
            TransactionSourcesNames.TRIGGER_JOB_EXECUTION,
            TransactionSourcesNames.GENERATE_IMAGE,
            TransactionSourcesNames.MODIFY_IMAGE,
            TransactionSourcesNames.VARIATE_IMAGE,
            TransactionSourcesNames.AUDIO_PROCESSING_STT,
            TransactionSourcesNames.AUDIO_PROCESSING_TTS,
        ]
