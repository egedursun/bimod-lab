#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: costs_map.py
#  Last Modified: 2024-10-05 02:20:19
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

from config.settings import COSTS_MAP


class ToolCostsMap:

    @staticmethod
    def as_list():
        return [
            ToolCostsMap.ContextMemory.COST,
            ToolCostsMap.ContextMemoryRetrieval.COST,
            ToolCostsMap.CodeInterpreter.COST,
            ToolCostsMap.DownloadExecutor.COST,
            ToolCostsMap.FileSystemsExecutor.COST,
            ToolCostsMap.KnowledgeBaseExecutor.COST,
            ToolCostsMap.CodeBaseExecutor.COST,
            ToolCostsMap.BrowsingExecutor.COST,
            ToolCostsMap.MLModelExecutor.COST,
            ToolCostsMap.InternalCustomFunctionExecutor.COST,
            ToolCostsMap.ExternalCustomFunctionExecutor.COST,
            ToolCostsMap.InternalCustomAPIExecutor.COST,
            ToolCostsMap.ExternalCustomAPIExecutor.COST,
            ToolCostsMap.InternalCustomScriptExecutor.COST,
            ToolCostsMap.ExternalCustomScriptExecutor.COST,
            ToolCostsMap.SQLReadExecutor.COST,
            ToolCostsMap.SQLWriteExecutor.COST,
            ToolCostsMap.FileInterpreter.COST,
            ToolCostsMap.ImageInterpreter.COST,
            ToolCostsMap.ScheduledJobExecutor.COST,
            ToolCostsMap.TriggeredJobExecutor.COST,
            ToolCostsMap.ImageGenerator.COST,
            ToolCostsMap.ImageModification.COST,
            ToolCostsMap.ImageVariation.COST,
            ToolCostsMap.AudioProcessingSTT.COST,
            ToolCostsMap.AudioProcessingTTS.COST,
            ToolCostsMap.VideoGenerator.COST,
            ToolCostsMap.Reasoning.COST,
        ]

    class ContextMemory:
        COST = COSTS_MAP["CONTEXT_MEMORY"]

    class ContextMemoryRetrieval:
        COST = COSTS_MAP["CONTEXT_MEMORY_RETRIEVAL"]

    class CodeInterpreter:
        COST = COSTS_MAP["CODE_INTERPRETER"]

    class DownloadExecutor:
        COST = COSTS_MAP["DOWNLOAD_EXECUTOR"]

    class FileSystemsExecutor:
        COST = COSTS_MAP["FILE_SYSTEMS_EXECUTOR"]

    class KnowledgeBaseExecutor:
        COST = COSTS_MAP["KNOWLEDGE_BASE_EXECUTOR"]

    class CodeBaseExecutor:
        COST = COSTS_MAP["CODE_BASE_EXECUTOR"]

    class BrowsingExecutor:
        COST = COSTS_MAP["BROWSING_EXECUTOR"]

    class MLModelExecutor:
        COST = COSTS_MAP["ML_MODEL_EXECUTOR"]

    class InternalCustomFunctionExecutor:
        COST = COSTS_MAP["INTERNAL_CUSTOM_FUNCTION_EXECUTOR"]

    class ExternalCustomFunctionExecutor:
        COST = COSTS_MAP["EXTERNAL_CUSTOM_FUNCTION_EXECUTOR"]

    class InternalCustomAPIExecutor:
        COST = COSTS_MAP["INTERNAL_CUSTOM_API_EXECUTOR"]

    class ExternalCustomAPIExecutor:
        COST = COSTS_MAP["EXTERNAL_CUSTOM_API_EXECUTOR"]

    class InternalCustomScriptExecutor:
        COST = COSTS_MAP["INTERNAL_CUSTOM_SCRIPT_EXECUTOR"]

    class ExternalCustomScriptExecutor:
        COST = COSTS_MAP["EXTERNAL_CUSTOM_SCRIPT_EXECUTOR"]

    class SQLReadExecutor:
        COST = COSTS_MAP["SQL_READ_EXECUTOR"]

    class SQLWriteExecutor:
        COST = COSTS_MAP["SQL_WRITE_EXECUTOR"]

    class FileInterpreter:
        COST = COSTS_MAP["FILE_INTERPRETER"]

    class ImageInterpreter:
        COST = COSTS_MAP["IMAGE_INTERPRETER"]

    class ScheduledJobExecutor:
        COST = COSTS_MAP["SCHEDULED_JOB_EXECUTOR"]

    class TriggeredJobExecutor:
        COST = COSTS_MAP["TRIGGERED_JOB_EXECUTOR"]

    class ImageGenerator:
        COST = COSTS_MAP["IMAGE_GENERATOR"]

    class ImageModification:
        COST = COSTS_MAP["IMAGE_MODIFICATION"]

    class ImageVariation:
        COST = COSTS_MAP["IMAGE_VARIATION"]

    class AudioProcessingSTT:
        COST = COSTS_MAP["AUDIO_PROCESSING_STT"]

    class AudioProcessingTTS:
        COST = COSTS_MAP["AUDIO_PROCESSING_TTS"]

    class VideoGenerator:
        COST = COSTS_MAP["VIDEO_GENERATOR"]

    class Reasoning:
        COST = COSTS_MAP["REASONING"]


"""
TRANSACTION_SOURCES = [
    ("app", "Application"),
    ("api", "API"),
    ("generation", "Generation"),
    ("sql-read", "SQL Read"),
    ("sql-write", "SQL Write"),
    ("store-memory", "Store Memory"),
    ("interpret-code", "Interpret Code"),
    ("reasoning", "Reasoning"),
    ("upload-file", "Upload File"),
    ("download-file", "Download File"),
    ("file-system-commands", "File System Commands"),
    ("knowledge-base-search", "Knowledge Base Search"),
    ("code-base-search", "Code Base Search"),
    ("retrieve-memory", "Retrieve Memory"),
    ("ml-model-prediction", "ML Model Prediction"),
    ("browsing", "Browsing"),
    ("internal-function-execution", "Internal Function Execution"),
    ("external-function-execution", "External Function Execution"),
    ("internal-api-execution", "Internal API Execution"),
    ("external-api-execution", "External API Execution"),
    ("internal-script-retrieval", "Internal Script Retrieval"),
    ("external-script-retrieval", "External Script Retrieval"),
    ("interpret-file", "Interpret File"),
    ("interpret-image", "Interpret Image"),
    ("scheduled-job-execution", "Scheduled Job Execution"),
    ("trigger-job-execution", "Trigger Job Execution"),
    ("generate-image", "Generate Image"),
    ("modify-image", "Modify Image"),
    ("variate-image", "Variate Image"),
    ("audio-processing-stt", "Audio Processing STT"),
    ("audio-processing-tts", "Audio Processing TTS"),
    ("brainstorming", "Brainstorming"),
    ("generate-video", "Generate Video"),
]
"""

TOOL_NAME_TO_COST_MAP = {
    "store-memory": ToolCostsMap.ContextMemory.COST,
    "retrieve-memory": ToolCostsMap.ContextMemoryRetrieval.COST,
    "interpret-code": ToolCostsMap.CodeInterpreter.COST,
    "download-file": ToolCostsMap.DownloadExecutor.COST,
    "file-system-commands": ToolCostsMap.FileSystemsExecutor.COST,
    "knowledge-base-search": ToolCostsMap.KnowledgeBaseExecutor.COST,
    "code-base-search": ToolCostsMap.CodeBaseExecutor.COST,
    "browsing": ToolCostsMap.BrowsingExecutor.COST,
    "ml-model-prediction": ToolCostsMap.MLModelExecutor.COST,
    "internal-function-execution": ToolCostsMap.InternalCustomFunctionExecutor.COST,
    "external-function-execution": ToolCostsMap.ExternalCustomFunctionExecutor.COST,
    "internal-api-execution": ToolCostsMap.InternalCustomAPIExecutor.COST,
    "external-api-execution": ToolCostsMap.ExternalCustomAPIExecutor.COST,
    "internal-script-retrieval": ToolCostsMap.InternalCustomScriptExecutor.COST,
    "external-script-retrieval": ToolCostsMap.ExternalCustomScriptExecutor.COST,
    "sql-read": ToolCostsMap.SQLReadExecutor.COST,
    "sql-write": ToolCostsMap.SQLWriteExecutor.COST,
    "interpret-file": ToolCostsMap.FileInterpreter.COST,
    "interpret-image": ToolCostsMap.ImageInterpreter.COST,
    "scheduled-job-execution": ToolCostsMap.ScheduledJobExecutor.COST,
    "trigger-job-execution": ToolCostsMap.TriggeredJobExecutor.COST,
    "generate-image": ToolCostsMap.ImageGenerator.COST,
    "modify-image": ToolCostsMap.ImageModification.COST,
    "variate-image": ToolCostsMap.ImageVariation.COST,
    "audio-processing-stt": ToolCostsMap.AudioProcessingSTT.COST,
    "audio-processing-tts": ToolCostsMap.AudioProcessingTTS.COST,
    "generate-video": ToolCostsMap.VideoGenerator.COST,
    "reasoning": ToolCostsMap.Reasoning.COST,
}
