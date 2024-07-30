

MULTIPLIER = 1


# Per Request
class ToolCostsMap:

    class ContextMemory:
        COST = 0.0100 * MULTIPLIER

    class ContextMemoryRetrieval:
        COST = 0.0050 * MULTIPLIER

    class CodeInterpreter:
        COST = 0.0100 * MULTIPLIER

    class DownloadExecutor:
        COST = 0.0050 * MULTIPLIER

    class FileSystemsExecutor:
        COST = 0.0100 * MULTIPLIER

    class KnowledgeBaseExecutor:
        COST = 0.0100 * MULTIPLIER

    class MLModelExecutor:
        COST = 0.0150 * MULTIPLIER

    class InternalCustomFunctionExecutor:
        COST = 0.0150 * MULTIPLIER

    class ExternalCustomFunctionExecutor:
        COST = 0.0075 * MULTIPLIER

    class InternalCustomAPIExecutor:
        COST = 0.0150 * MULTIPLIER

    class ExternalCustomAPIExecutor:
        COST = 0.0075 * MULTIPLIER

    class InternalCustomScriptRetriever:
        COST = 0.0050 * MULTIPLIER

    class ExternalCustomScriptRetriever:
        COST = 0.0025 * MULTIPLIER

    class SQLReadExecutor:
        COST = 0.0050 * MULTIPLIER

    class SQLWriteExecutor:
        COST = 0.0100 * MULTIPLIER

    class FileInterpreter:
        COST = 0.0050 * MULTIPLIER

    class ImageInterpreter:
        COST = 0.0100 * MULTIPLIER

    class ScheduledJobExecutor:
        COST = 0.0050 * MULTIPLIER

    class ImageGenerator:
        COST = 0.0050 * MULTIPLIER

    class ImageModification:
        COST = 0.0025 * MULTIPLIER

    class ImageVariation:
        COST = 0.0025 * MULTIPLIER






