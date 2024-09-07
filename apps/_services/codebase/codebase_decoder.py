from apps._services.codebase.codebase_executor import WeaviateExecutor


class CodeBaseDecoder:
    KNOWLEDGE_BASE_PROVIDERS = {
        "WEAVIATE": {
            "code": "weaviate",
            "name": "Weaviate"
        },
    }

    @staticmethod
    def get(connection):
        if connection.provider == CodeBaseDecoder.KNOWLEDGE_BASE_PROVIDERS["WEAVIATE"]["code"]:
            print(f"[CodeBaseDecoder.get] Weaviate provider selected.")
            return WeaviateExecutor(connection)
