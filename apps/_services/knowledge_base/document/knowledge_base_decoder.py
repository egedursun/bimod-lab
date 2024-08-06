from apps._services.knowledge_base.document.knowledge_base_executor import WeaviateExecutor


class KnowledgeBaseSystemDecoder:
    KNOWLEDGE_BASE_PROVIDERS = {
        "WEAVIATE": {
            "code": "weaviate",
            "name": "Weaviate"
        },
    }

    @staticmethod
    def get(connection):
        if connection.provider == KnowledgeBaseSystemDecoder.KNOWLEDGE_BASE_PROVIDERS["WEAVIATE"]["code"]:
            print(f"[KnowledgeBaseSystemDecoder.get] Weaviate provider selected.")
            return WeaviateExecutor(connection)
