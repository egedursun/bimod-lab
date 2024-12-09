#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from config.settings import COSTS_MAP


class InternalServiceCosts:

    @staticmethod
    def as_list():
        return [
            InternalServiceCosts.ContextMemory.COST,
            InternalServiceCosts.ContextMemoryRetrieval.COST,
            InternalServiceCosts.CodeInterpreter.COST,
            InternalServiceCosts.DownloadExecutor.COST,
            InternalServiceCosts.FileSystemsExecutor.COST,
            InternalServiceCosts.KnowledgeBaseExecutor.COST,
            InternalServiceCosts.CodeBaseExecutor.COST,
            InternalServiceCosts.BrowsingExecutor.COST,
            InternalServiceCosts.MLModelExecutor.COST,
            InternalServiceCosts.InternalCustomFunctionExecutor.COST,
            InternalServiceCosts.ExternalCustomFunctionExecutor.COST,
            InternalServiceCosts.InternalCustomAPIExecutor.COST,
            InternalServiceCosts.ExternalCustomAPIExecutor.COST,
            InternalServiceCosts.InternalCustomScriptExecutor.COST,
            InternalServiceCosts.ExternalCustomScriptExecutor.COST,
            InternalServiceCosts.SQLReadExecutor.COST,
            InternalServiceCosts.SQLWriteExecutor.COST,
            InternalServiceCosts.NoSQLReadExecutor.COST,
            InternalServiceCosts.NoSQLWriteExecutor.COST,
            InternalServiceCosts.FileInterpreter.COST,
            InternalServiceCosts.ImageInterpreter.COST,
            InternalServiceCosts.ScheduledJobExecutor.COST,
            InternalServiceCosts.TriggeredJobExecutor.COST,
            InternalServiceCosts.ImageGenerator.COST,
            InternalServiceCosts.ImageModification.COST,
            InternalServiceCosts.ImageVariation.COST,
            InternalServiceCosts.AudioProcessingSTT.COST,
            InternalServiceCosts.AudioProcessingTTS.COST,
            InternalServiceCosts.VideoGenerator.COST,
            InternalServiceCosts.Reasoning.COST,
            InternalServiceCosts.Drafting.COST,
            InternalServiceCosts.Sheetos.COST,
            InternalServiceCosts.Formica.COST,
            InternalServiceCosts.Slider.COST,
            InternalServiceCosts.HadronPrime.COST,
            InternalServiceCosts.SmartContractCreation.COST,
            InternalServiceCosts.Binexus.COST,
            InternalServiceCosts.MetaKanban.COST,
            InternalServiceCosts.MeetingTranscription.COST,
            InternalServiceCosts.MetaTempo.COST,
            InternalServiceCosts.EllmaScripting.COST,
            InternalServiceCosts.WebsiteStorageExecutor.COST,
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

    class NoSQLReadExecutor:
        COST = COSTS_MAP["NOSQL_READ_EXECUTOR"]

    class NoSQLWriteExecutor:
        COST = COSTS_MAP["NOSQL_WRITE_EXECUTOR"]

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

    class EllmaScripting:
        COST = COSTS_MAP["ELLMA_SCRIPTING"]

    class Drafting:
        COST = COSTS_MAP["DRAFTING"]

    class Sheetos:
        COST = COSTS_MAP["SHEETOS"]

    class Formica:
        COST = COSTS_MAP["FORMICA"]

    class Slider:
        COST = COSTS_MAP["SLIDER"]

    class HadronPrime:
        COST = COSTS_MAP["HADRON_PRIME"]

    class SmartContractCreation:
        COST = COSTS_MAP["SMART_CONTRACT_CREATION"]

    class Binexus:
        COST = COSTS_MAP["BINEXUS"]

    class MetaKanban:
        COST = COSTS_MAP["METAKANBAN"]

    class MeetingTranscription:
        COST = COSTS_MAP["MEETING_TRANSCRIPTION"]

    class MetaTempo:
        COST = COSTS_MAP["METATEMPO"]

    class WebsiteStorageExecutor:
        COST = COSTS_MAP["WEBSITE_STORAGE_EXECUTOR"]


TOOL_NAME_TO_COST_MAP = {
    "store-memory": InternalServiceCosts.ContextMemory.COST,
    "retrieve-memory": InternalServiceCosts.ContextMemoryRetrieval.COST,
    "interpret-code": InternalServiceCosts.CodeInterpreter.COST,
    "download-file": InternalServiceCosts.DownloadExecutor.COST,
    "file-system-commands": InternalServiceCosts.FileSystemsExecutor.COST,
    "knowledge-base-search": InternalServiceCosts.KnowledgeBaseExecutor.COST,
    "code-base-search": InternalServiceCosts.CodeBaseExecutor.COST,
    "browsing": InternalServiceCosts.BrowsingExecutor.COST,
    "ml-model-prediction": InternalServiceCosts.MLModelExecutor.COST,
    "internal-function-execution": InternalServiceCosts.InternalCustomFunctionExecutor.COST,
    "external-function-execution": InternalServiceCosts.ExternalCustomFunctionExecutor.COST,
    "internal-api-execution": InternalServiceCosts.InternalCustomAPIExecutor.COST,
    "external-api-execution": InternalServiceCosts.ExternalCustomAPIExecutor.COST,
    "internal-script-retrieval": InternalServiceCosts.InternalCustomScriptExecutor.COST,
    "external-script-retrieval": InternalServiceCosts.ExternalCustomScriptExecutor.COST,
    "sql-read": InternalServiceCosts.SQLReadExecutor.COST,
    "sql-write": InternalServiceCosts.SQLWriteExecutor.COST,
    "nosql-read": InternalServiceCosts.NoSQLReadExecutor.COST,
    "nosql-write": InternalServiceCosts.NoSQLWriteExecutor.COST,
    "interpret-file": InternalServiceCosts.FileInterpreter.COST,
    "interpret-image": InternalServiceCosts.ImageInterpreter.COST,
    "scheduled-job-execution": InternalServiceCosts.ScheduledJobExecutor.COST,
    "trigger-job-execution": InternalServiceCosts.TriggeredJobExecutor.COST,
    "generate-image": InternalServiceCosts.ImageGenerator.COST,
    "modify-image": InternalServiceCosts.ImageModification.COST,
    "variate-image": InternalServiceCosts.ImageVariation.COST,
    "audio-processing-stt": InternalServiceCosts.AudioProcessingSTT.COST,
    "audio-processing-tts": InternalServiceCosts.AudioProcessingTTS.COST,
    "generate-video": InternalServiceCosts.VideoGenerator.COST,
    "reasoning": InternalServiceCosts.Reasoning.COST,
    "ellma-scripting": InternalServiceCosts.EllmaScripting.COST,
    "drafting": InternalServiceCosts.Drafting.COST,
    "sheetos": InternalServiceCosts.Sheetos.COST,
    "formica": InternalServiceCosts.Formica.COST,
    "slider": InternalServiceCosts.Slider.COST,
    "hadron-prime": InternalServiceCosts.HadronPrime.COST,
    "smart-contract-creation": InternalServiceCosts.SmartContractCreation.COST,
    "binexus": InternalServiceCosts.Binexus.COST,
    "metakanban": InternalServiceCosts.MetaKanban.COST,
    "meeting-transcription": InternalServiceCosts.MeetingTranscription.COST,
    "metatempo": InternalServiceCosts.MetaTempo.COST,
    "website-storage-executor": InternalServiceCosts.WebsiteStorageExecutor.COST,
}
