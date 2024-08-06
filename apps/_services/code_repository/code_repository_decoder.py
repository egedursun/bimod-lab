from apps._services.code_repository.code_repository_executor import WeaviateExecutor


class CodeRepositorySystemDecoder:
    CODE_REPOSITORY_PROVIDERS = {
        "WEAVIATE": {
            "code": "weaviate",
            "name": "Weaviate"
        },
    }

    @staticmethod
    def get(connection):
        if connection.provider == CodeRepositorySystemDecoder.CODE_REPOSITORY_PROVIDERS["WEAVIATE"]["code"]:
            print("[CodeRepositorySystemDecoder.get] Weaviate code repository provider selected.")
            return WeaviateExecutor(connection)
