#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ner_mtest.py
#  Last Modified: 2024-10-05 20:35:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:09:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import spacy
from collections import defaultdict

NER_MODEL_NAME_DESCRIPTOR = "en_core_web_md"

nlp = None
try:
    nlp = spacy.load(NER_MODEL_NAME_DESCRIPTOR)
except OSError:
    try:
        from spacy.cli.download import download
        download(NER_MODEL_NAME_DESCRIPTOR)
        nlp = spacy.load(NER_MODEL_NAME_DESCRIPTOR)
    except Exception as e:
        pass


def anonymize_text(text):
    doc = nlp(text)
    entity_mapping = defaultdict(dict)
    anonymized_tokens = []
    entity_counters = {
        "PERSON": 0,
        "ORG": 0,
        "GPE": 0,
        "DATE": 0,
        "CARDINAL": 0
    }

    for token in doc:
        entity_type = token.ent_type_
        if entity_type in entity_counters:
            placeholder = f"[{entity_type}_{entity_counters[entity_type]}]"
            entity_mapping[entity_type][placeholder] = token.text
            anonymized_tokens.append(placeholder)
            entity_counters[entity_type] += 1
        else:
            anonymized_tokens.append(token.text)

    anonymized_text = " ".join(anonymized_tokens)
    return anonymized_text, entity_mapping


def deanonymize_text(anonymized_text, entity_mapping):
    tokens = anonymized_text.split()
    deanonymized_tokens = []

    for token in tokens:
        for entity_type, mappings in entity_mapping.items():
            if token in mappings:
                deanonymized_tokens.append(mappings[token])
                break
        else:
            deanonymized_tokens.append(token)

    return " ".join(deanonymized_tokens)


text = "John Doe works at OpenAI in San Francisco. He was born on January 1, 1980."
anonymized_text, entity_mapping = anonymize_text(text)

print("Original Text:")
print(text)
print("\nAnonymized Text:")
print(anonymized_text)
print("\nEntity Mapping:")
print(entity_mapping)
de_anonymized_text = deanonymize_text(anonymized_text, entity_mapping)
print(de_anonymized_text)
