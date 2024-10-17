#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
import logging
from collections import defaultdict

from apps.core.data_security.ner.utils import DEFAULT_MODEL, LANGUAGE_TO_MODEL_MAPPING
from apps.data_security.models import NERIntegration
import spacy


logger = logging.getLogger(__name__)


class NERExecutor:
    def __init__(self, ner_id: int):
        try:
            self.ner_integration: NERIntegration = NERIntegration.objects.get(id=ner_id)
            logger.info(f"NERIntegration: {self.ner_integration}")
        except Exception as e:
            logger.error(f"Error fetching NERIntegration: {e}")
            pass
        try:
            self.model = self._decode_model_from_language(self.ner_integration.language)
            logger.info(f"Model: {self.model}")
        except Exception as e:
            logger.error(f"Error decoding model: {e}")
            pass
        try:
            self.nlp = self._load_model(self.model)
            logger.info(f"Loaded model: {self.nlp}")
            if not self.nlp:
                logger.error("[NERExecutor.__init__] Error loading model.")
                raise Exception("Error loading model.")
        except Exception as e:
            logger.error(f"Error loading model: {e}")

        #__________________________________________________________________________________________________#
        # Temporary Storage for Entity Mappings
        self.entity_mapping = defaultdict(dict)
        #__________________________________________________________________________________________________#

    @staticmethod
    def _decode_model_from_language(language: str) -> str:
        return LANGUAGE_TO_MODEL_MAPPING.get(language, DEFAULT_MODEL)

    @staticmethod
    def _load_model(model_name: str):
        nlp = None
        try:
            nlp = spacy.load(model_name)
            logger.info(f"Loaded model: {model_name}")
        except OSError:
            try:
                from spacy.cli.download import download
                download(model_name)
                nlp = spacy.load(model_name)
                logger.info(f"Downloaded and loaded model: {model_name}")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                pass
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
        logger.info(f"Entity Mapping: {entity_mapping}")
        return entity_mapping

    def encrypt_text(self, text: str, uuid_str: str) -> str:
        doc = self.nlp(text)
        self.entity_mapping[uuid_str] = {}
        anonymized_text = text
        entity_counters = self.build_entity_mapping()
        for ent in doc.ents:
            entity_type = ent.label_
            if entity_type in entity_counters:
                placeholder = f"<[[{entity_type}_{entity_counters[entity_type]}]]>"
                self.entity_mapping[uuid_str][placeholder] = ent.text
                anonymized_text = anonymized_text.replace(ent.text, placeholder)
                entity_counters[entity_type] += 1
        logger.info(f"Anonymized Text retrieved.")
        return anonymized_text

    def decrypt_text(self, anonymized_text: str, uuid: str) -> str:
        deanonymized_text = anonymized_text
        for placeholder, original_text in self.entity_mapping.get(uuid, {}).items():
            deanonymized_text = deanonymized_text.replace(placeholder, original_text)

        try:
            self.entity_mapping.pop(uuid, None)
            logger.info(f"De-anonymized Text retrieved.")
        except Exception as e:
            logger.error(f"Error de-anonymizing text: {e}")
            pass
        return deanonymized_text
