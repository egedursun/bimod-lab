#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: ner_executor.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from collections import defaultdict

from apps._services.data_security.ner.utils import DEFAULT_MODEL, LANGUAGE_TO_MODEL_MAPPING
from apps.data_security.models import NERIntegration
import spacy


class NERExecutor:
    def __init__(self, ner_id: int):
        try:
            self.ner_integration: NERIntegration = NERIntegration.objects.get(id=ner_id)
        except Exception as e:
            print("[NERExecutor.__init__] Error loading NERIntegration:", e)
        try:
            self.model = self._decode_model_from_language(self.ner_integration.language)
        except Exception as e:
            print("[NERExecutor.__init__] Error decoding model from language:", e)
        try:
            self.nlp = self._load_model(self.model)
            if not self.nlp:
                raise Exception("[NERExecutor.__init__] Error loading model.")
        except Exception as e:
            print("[NERExecutor.__init__] Error loading model:", e)

        ####################################################################################################
        # Temporary Storage for Entity Mappings
        ####################################################################################################
        self.entity_mapping = defaultdict(dict)
        ####################################################################################################

    @staticmethod
    def _decode_model_from_language(language: str) -> str:
        return LANGUAGE_TO_MODEL_MAPPING.get(language, DEFAULT_MODEL)

    @staticmethod
    def _load_model(model_name: str):
        nlp = None
        try:
            nlp = spacy.load(model_name)
            print("[NERExecutor._load_model] Successfully Loaded the SpaCy model.")
        except OSError:
            try:
                print("[NERExecutor._load_model] Downloading the SpaCy model...")
                from spacy.cli.download import download
                download(model_name)
                print("[NERExecutor._load_model] Downloaded the SpaCy model.")
                nlp = spacy.load(model_name)
                print("[NERExecutor._load_model] Successfully Loaded the SpaCy model.")
            except Exception as e:
                print("Error downloading the SpaCy model:", e)
        return nlp

    def build_entity_mapping(self):
        entity_mapping = {}
        if self.ner_integration.encrypt_persons is True:
            entity_mapping['PERSON'] = 0
        if self.ner_integration.encrypt_orgs is True:
            entity_mapping['ORG'] = 0
        if self.ner_integration.encrypt_nationality_religion_political is True:
            entity_mapping['NORP'] = 0
        if self.ner_integration.encrypt_facilities is True:
            entity_mapping['FAC'] = 0
        if self.ner_integration.encrypt_countries_cities_states is True:
            entity_mapping['GPE'] = 0
        if self.ner_integration.encrypt_locations is True:
            entity_mapping['LOC'] = 0
        if self.ner_integration.encrypt_products is True:
            entity_mapping['PRODUCT'] = 0
        if self.ner_integration.encrypt_events is True:
            entity_mapping['EVENT'] = 0
        if self.ner_integration.encrypt_artworks is True:
            entity_mapping['WORK_OF_ART'] = 0
        if self.ner_integration.encrypt_laws is True:
            entity_mapping['LAW'] = 0
        if self.ner_integration.encrypt_languages is True:
            entity_mapping['LANGUAGE'] = 0
        if self.ner_integration.encrypt_dates is True:
            entity_mapping['DATE'] = 0
        if self.ner_integration.encrypt_times is True:
            entity_mapping['TIME'] = 0
        if self.ner_integration.encrypt_percentages is True:
            entity_mapping['PERCENT'] = 0
        if self.ner_integration.encrypt_money is True:
            entity_mapping['MONEY'] = 0
        if self.ner_integration.encrypt_quantities is True:
            entity_mapping['QUANTITY'] = 0
        if self.ner_integration.encrypt_ordinal_numbers is True:
            entity_mapping['ORDINAL'] = 0
        if self.ner_integration.encrypt_cardinal_numbers is True:
            entity_mapping['CARDINAL'] = 0
        return entity_mapping

    def encrypt_text(self, text: str, uuid_str: str) -> str:
        doc = self.nlp(text)
        # Dictionary to store entity mappings
        self.entity_mapping[uuid_str] = {}
        anonymized_text = text
        entity_counters = self.build_entity_mapping()

        for ent in doc.ents:
            entity_type = ent.label_
            if entity_type in entity_counters:
                # Generate a unique placeholder with a more complex format
                placeholder = f"<[[{entity_type}_{entity_counters[entity_type]}]]>"

                # Store the mapping between the placeholder and the original text
                self.entity_mapping[uuid_str][placeholder] = ent.text

                # Replace the entity in the text with the placeholder
                anonymized_text = anonymized_text.replace(ent.text, placeholder)

                entity_counters[entity_type] += 1

        print("[NERExecutor.encrypt_text] Anonymized Text: \n", anonymized_text)
        return anonymized_text

    def decrypt_text(self, anonymized_text: str, uuid: str) -> str:
        deanonymized_text = anonymized_text

        # Replace the placeholders with the original entities
        for placeholder, original_text in self.entity_mapping.get(uuid, {}).items():
            # Replace all occurrences of the placeholder with the original text
            deanonymized_text = deanonymized_text.replace(placeholder, original_text)

        print("[NERExecutor.decrypt_text] De-anonymized Text: \n", deanonymized_text)

        # Clean the entity mapping
        try:
            self.entity_mapping.pop(uuid, None)
            print("[NERExecutor.decrypt_text] Entity Mapping cleaned.")
        except Exception as e:
            print("[NERExecutor.decrypt_text] Error cleaning entity mapping:", e)

        return deanonymized_text
