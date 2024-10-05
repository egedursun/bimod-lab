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
            ToolCostsMap.VideoGenerator.COST
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
