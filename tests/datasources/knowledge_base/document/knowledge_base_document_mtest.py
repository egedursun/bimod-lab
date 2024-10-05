#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#

from pprint import pprint

import weaviate
from weaviate.config import AdditionalConfig, Timeout

kb_id = 16  # change this based on the test knowledge base

host = "https://meebjrn0qb228tw9gaxeia.c0.europe-west3.gcp.weaviate.cloud"
api_key = "H5ePQ4TyNDJy0dFsf4pqo9Gbf7xZo0eo42Q9"
vectorizer_api_key = "sk-proj-AfSj7ohaxbXDQf2WLLSUT3BlbkFJGZifjSfVePMOJtBeRz5V"

client = weaviate.connect_to_weaviate_cloud(
                cluster_url=host,
                auth_credentials=weaviate.auth.AuthApiKey(api_key=api_key),
                headers={
                    "X-OpenAI-Api-Key": vectorizer_api_key
                },
                additional_config=AdditionalConfig(
                    timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
                )
            )

# try generative search with hybrid
documents_collection = client.collections.get(f"TestweaviateShantyTermiteNutmeg2074812Chunks")
response = documents_collection.query.hybrid(
    query_properties=["chunk_document_file_name", "chunk_content"],
    query="who is mert tekin?",
    alpha=float(0.5),
    limit=10
)

client.close()

# clean the response
cleaned_documents = []
for o in response.objects:
    cleaned_object = {}
    if not o.properties:
        continue
    for k, v in o.properties.items():
        if k in ["chunk_document_file_name", "chunk_content", "chunk_number", "created_at"]:
            cleaned_object[k] = v
    cleaned_documents.append(cleaned_object)

pprint(cleaned_documents)
