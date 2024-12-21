#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: weaviate_dummy_data.py
#  Last Modified: 2024-12-20 20:32:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-20 20:32:20
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import os

import weaviate

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("INTERNAL_OPENAI_API_KEY")

# Connect to Weaviate with its API key
client = weaviate.Client(
    url="https://bs0ibgkjsr6iocfzjbagnw.c0.us-east1.gcp.weaviate.cloud",
    additional_headers={
        "Authorization": "Bearer rdbu6uJVIYu1aRZaoIlRXYQ6yovYtg1ZDlAd",
        "X-OpenAI-Api-Key": OPENAI_API_KEY,
    }
)

schema = {
    "classes": [
        {
            "class": "Sentence",
            "description": "A collection of sentences with OpenAI embeddings",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "text-embedding-3-large",
                    "type": "text"
                }
            },
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The content of the sentence"
                },
                {
                    "name": "category",
                    "dataType": ["text"],
                    "description": "Category of the sentence"
                }
            ]
        }
    ]
}

client.schema.delete_all()

client.schema.create(schema)

dummy_sentences = [
    {
        "content": "Weaviate is a vector database.",
        "category": "Tech"
    },
    {
        "content": "I love machine learning.",
        "category": "Education"
    },
    {
        "content": "This is a test sentence.",
        "category": "General"
    },
    {
        "content": "Data science is fascinating.",
        "category": "Education"
    }
]

for sentence in dummy_sentences:
    client.data_object.create(
        data_object=sentence,
        class_name="Sentence"
    )

print("Dummy sentences indexed successfully!")
