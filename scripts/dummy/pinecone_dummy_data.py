import numpy as np

from dotenv import load_dotenv

from pinecone import (
    Pinecone,
    ServerlessSpec
)

from apps.datasource_nosql.utils import (
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

load_dotenv()

PINECONE_API_KEY = "..."
ENVIRONMENT = "multilingual-e5-large"
AWS_REGION = "us-east-1"

INDEX_NAME = "test-index"

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=AWS_REGION,
        )
    )

index = pc.Index(
    INDEX_NAME
)


def generate_dummy_data(
    num_vectors=1000,
    vector_dim=OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
):
    data = []
    for i in range(num_vectors):
        vector = np.random.random(
            vector_dim
        ).tolist()

        metadata = {
            "id": f"vector_{i}",
            "category": "dummy",
            "value": np.random.randint(
                1,
                100
            )
        }
        data.append(
            (
                f"id_{i}",
                vector,
                metadata
            )
        )

    return data


def upsert_in_batches(
    index,
    data,
    batch_size=100
):
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        index.upsert(
            vectors=batch
        )
        print(f"Upserted batch {i // batch_size + 1}")


dummy_data = generate_dummy_data(
    num_vectors=1000,
)

upsert_in_batches(
    index,
    dummy_data,
    batch_size=100
)

print("Dummy data inserted successfully!")
