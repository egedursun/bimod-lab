#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#

import spacy
from collections import defaultdict

MODEL_NAME = "en_core_web_md"

####################################################################################################
# Load the pre-trained SpaCy model for English
nlp = None
try:
    nlp = spacy.load(MODEL_NAME)
except OSError:
    try:
        print("Downloading the SpaCy model for English...")
        from spacy.cli.download import download
        download(MODEL_NAME)
        nlp = spacy.load(MODEL_NAME)
    except Exception as e:
        print("Error downloading the SpaCy model for English:", e)
        pass
####################################################################################################


# Function to anonymize text with reversible mapping
def anonymize_text(text):
    doc = nlp(text)

    # Dictionary to store entity mappings
    entity_mapping = defaultdict(dict)
    anonymized_tokens = []

    # Counters to create unique placeholders
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
            # Generate a unique placeholder for each entity
            placeholder = f"[{entity_type}_{entity_counters[entity_type]}]"
            entity_mapping[entity_type][placeholder] = token.text

            anonymized_tokens.append(placeholder)
            entity_counters[entity_type] += 1
        else:
            anonymized_tokens.append(token.text)

    anonymized_text = " ".join(anonymized_tokens)
    return anonymized_text, entity_mapping


# Function to reverse the anonymization using the mapping
def deanonymize_text(anonymized_text, entity_mapping):
    tokens = anonymized_text.split()
    deanonymized_tokens = []

    for token in tokens:
        # Check if token is a placeholder and replace it with the original entity
        for entity_type, mappings in entity_mapping.items():
            if token in mappings:
                deanonymized_tokens.append(mappings[token])
                break
        else:
            deanonymized_tokens.append(token)

    return " ".join(deanonymized_tokens)


# Example text with sensitive information
text = "John Doe works at OpenAI in San Francisco. He was born on January 1, 1980."

# Anonymize the text
anonymized_text, entity_mapping = anonymize_text(text)

print("Original Text:")
print(text)
print("\nAnonymized Text:")
print(anonymized_text)
print("\nEntity Mapping:")
print(entity_mapping)

# Reverse the anonymization
deanonymized_text = deanonymize_text(anonymized_text, entity_mapping)
print("\nDe-anonymized Text:")
print(deanonymized_text)
