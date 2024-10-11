#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: code_interpreter_executor.py
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

from apps.core.code_analyst.utils import save_files_and_return_uris, save_images_and_return_uris
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


class CodeAnalystExecutionManager:

    def __init__(self, assistant, chat):
        self.assistant = assistant
        self.chat = chat

    def analyze_code_script(self, full_file_paths: list, query_string: str):
        from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_code_analysis_client import \
            AuxiliaryLLMCodeAnalysisManager
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        try:
            llm_c = AuxiliaryLLMCodeAnalysisManager(assistant=self.assistant, chat_object=self.chat)
        except Exception as e:
            return None

        try:
            txt, fs, ims = llm_c.analyze_code_script(full_file_paths=full_file_paths,
                                                     query_string=query_string,
                                                     interpretation_temperature=float(self.assistant.llm_model.temperature))
        except Exception as e:
            return None, None, None

        try:
            final_f_uris = save_files_and_return_uris(fs)
            final_img_uris = save_images_and_return_uris(ims)
        except Exception as e:
            return None, None, None

        llm_output = {"response": txt, "file_uris": final_f_uris, "image_uris": final_img_uris}
        try:
            tx = LLMTransaction(
                organization=self.chat.assistant.organization, model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, llm_cost=InternalServiceCosts.CodeInterpreter.COST,
                transaction_type=ChatRoles.SYSTEM, transaction_source=LLMTransactionSourcesTypesNames.INTERPRET_CODE,
                is_tool_cost=True)
            tx.save()

        except Exception as e:
            return None, None, None
        return llm_output
