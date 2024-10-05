#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: brainstorms_executor.py
#  Last Modified: 2024-10-01 16:10:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: brainstorms_executor.py
#  Last Modified: 2024-10-01 01:05:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 01:05:49
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#

from openai import OpenAI

from apps._services.brainstorms.utils import build_from_scratch_brainstorms_system_prompt, find_json_presence, \
    build_from_previous_level_brainstorms_system_prompt, build_synthesis_from_level_system_prompt, \
    build_synthesis_from_all_levels_system_prompt
from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames


class BrainstormsExecutor:
    from apps.brainstorms.models import BrainstormingSession

    def __init__(self, session: BrainstormingSession):
        self.session = session
        self.client = OpenAI(api_key=self.session.llm_model.api_key)

    def _generate_llm_response(self, system_prompt: str):
        from apps._services.llms.utils import ChatRoles
        system_message = {"role": ChatRoles.SYSTEM.lower(), "content": system_prompt}

        LLMTransaction.objects.create(
            organization=self.session.organization,
            model=self.session.llm_model,
            responsible_user=self.session.created_by_user,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=system_prompt,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.BRAINSTORMING,
        )

        choice_message_content = None
        try:
            llm_response = self.client.chat.completions.create(
                model=self.session.llm_model.model_name,
                messages=[system_message],
                temperature=float(self.session.llm_model.temperature),
                frequency_penalty=float(self.session.llm_model.frequency_penalty),
                presence_penalty=float(self.session.llm_model.presence_penalty),
                max_tokens=int(self.session.llm_model.maximum_tokens),
                top_p=float(self.session.llm_model.top_p),
            )
            print(f"[BrainstormsExecutor._generate_llm_response] Retrieved the response from the LLM.")
            choices = llm_response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            print(f"[BrainstormsExecutor._generate_llm_response] Extracted the response content from the LLM.")
        except Exception as e:
            print(
                f"[BrainstormsExecutor._generate_llm_response] An error occurred while retrieving the response from"
                f"the LLM: {e}")
        final_response = choice_message_content
        return final_response

    def _create_idea_objects_with_llm_response(self, llm_response: str, depth_level: int):
        from apps.brainstorms.models import BrainstormingIdea
        elements = []
        try:
            elements = find_json_presence(response=llm_response)
        except Exception as e:
            print(f"[BrainstormsExecutor._create_idea_objects_with_llm_response] Error parsing the JSON: {e}")

        for element in elements:
            try:
                session = self.session
                created_by_user = session.created_by_user
                idea_title = element.get("idea_title")
                idea_description = element.get("idea_description")
                is_bookmarked = False
                BrainstormingIdea.objects.create(
                    brainstorming_session=session,
                    created_by_user=created_by_user,
                    idea_title=idea_title,
                    idea_description=idea_description,
                    depth_level=depth_level,
                    is_bookmarked=is_bookmarked)
            except Exception as e:
                print(
                    f"[BrainstormsExecutor._create_idea_objects_with_llm_response] Error creating the idea object: {e}")
                continue

        print(f"[BrainstormsExecutor._create_idea_objects_with_llm_response] Created the idea objects successfully.")
        return

    def _create_level_synthesis_object_with_llm_response(self, llm_response: str, depth_level: int):
        from apps.brainstorms.models import BrainstormingLevelSynthesis

        element = None
        try:
            element = find_json_presence(response=llm_response)[0]
        except Exception as e:
            print(
                f"[BrainstormsExecutor._create_level_synthesis_object_with_llm_response] Error parsing the JSON: {e}")
            return

        try:
            session = self.session
            created_by_user = session.created_by_user
            synthesis_content = element.get("synthesis_content")
            BrainstormingLevelSynthesis.objects.create(
                brainstorming_session=session,
                created_by_user=created_by_user,
                synthesis_content=synthesis_content,
                depth_level=depth_level)
        except Exception as e:
            print(f"[BrainstormsExecutor._create_level_synthesis_object_with_llm_response] Error creating the "
                  f"level synthesis object: {e}")
            return

        print(f"[BrainstormsExecutor._create_level_synthesis_object_with_llm_response] Created the level synthesis "
              f"object successfully.")
        return

    def _create_complete_synthesis_object_with_llm_response(self, llm_response: str):
        from apps.brainstorms.models import BrainstormingCompleteSynthesis
        element = None
        try:
            element = find_json_presence(response=llm_response)[0]
        except Exception as e:
            print(
                f"[BrainstormsExecutor._create_complete_synthesis_object_with_llm_response] Error parsing the JSON: {e}")
            return

        try:
            session = self.session
            created_by_user = session.created_by_user
            synthesis_content = element.get("synthesis_content")
            BrainstormingCompleteSynthesis.objects.create(
                brainstorming_session=session,
                created_by_user=created_by_user,
                synthesis_content=synthesis_content)
        except Exception as e:
            print(f"[BrainstormsExecutor._create_complete_synthesis_object_with_llm_response] Error creating the "
                  f"complete synthesis object: {e}")
            return

        print(f"[BrainstormsExecutor._create_complete_synthesis_object_with_llm_response] Created the complete "
              f"synthesis object successfully.")
        return

    #################################################################################################################

    def produce_ideas(self, depth_level=1):
        from apps.brainstorms.models import BrainstormingIdea
        try:
            if depth_level == 1:
                system_prompt = build_from_scratch_brainstorms_system_prompt(session=self.session)
                response_text = self._generate_llm_response(system_prompt)
                self._create_idea_objects_with_llm_response(llm_response=response_text, depth_level=depth_level)
            else:
                previous_depth_level = (depth_level - 1)
                previous_level_bookmarked_ideas = BrainstormingIdea.objects.filter(
                    brainstorming_session=self.session, depth_level=previous_depth_level, is_bookmarked=True)
                system_prompt = build_from_previous_level_brainstorms_system_prompt(session=self.session,
                                                                                    previous_level_bookmarked_ideas=previous_level_bookmarked_ideas)
                response_text = self._generate_llm_response(system_prompt)
                self._create_idea_objects_with_llm_response(llm_response=response_text, depth_level=depth_level)
        except Exception as e:
            print(f"[BrainstormsExecutor.produce_ideas] An error occurred while producing ideas: {e}")
            return
        print(f"[BrainstormsExecutor.produce_ideas] Ideas have been produced successfully.")
        return

    def generate_level_synthesis(self, depth_level):
        from apps.brainstorms.models import BrainstormingIdea, BrainstormingLevelSynthesis
        try:
            # Remove all existing level syntheses for the given depth level (if any)
            existing_syntheses = BrainstormingLevelSynthesis.objects.filter(
                brainstorming_session=self.session, depth_level=depth_level)
            if existing_syntheses.exists():
                existing_syntheses.delete()  # This will delete all found entries for this level
                print(
                    f"[BrainstormsExecutor.generate_level_synthesis] Existing level syntheses for depth {depth_level} removed.")

            depth_level_bookmarked_ideas = BrainstormingIdea.objects.filter(
                brainstorming_session=self.session, depth_level=depth_level, is_bookmarked=True)
            system_prompt = build_synthesis_from_level_system_prompt(session=self.session,
                                                                     bookmarked_ideas=depth_level_bookmarked_ideas)
            response_text = self._generate_llm_response(system_prompt)
            self._create_level_synthesis_object_with_llm_response(llm_response=response_text, depth_level=depth_level)
        except Exception as e:
            print(
                f"[BrainstormsExecutor.generate_level_synthesis] An error occurred while generating the level synthesis for depth {depth_level}: {e}")
            return
        print(
            f"[BrainstormsExecutor.generate_level_synthesis] Level synthesis for depth {depth_level} has been generated successfully.")
        return

    def generate_complete_synthesis(self):
        from apps.brainstorms.models import BrainstormingIdea, BrainstormingCompleteSynthesis
        try:
            # Remove all existing complete syntheses (if any)
            existing_syntheses = BrainstormingCompleteSynthesis.objects.filter(brainstorming_session=self.session)
            if existing_syntheses.exists():
                existing_syntheses.delete()  # This will delete all found entries
                print(f"[BrainstormsExecutor.generate_complete_synthesis] Existing complete syntheses removed.")

            bookmarked_ideas = BrainstormingIdea.objects.filter(
                brainstorming_session=self.session, is_bookmarked=True)
            system_prompt = build_synthesis_from_all_levels_system_prompt(session=self.session,
                                                                          bookmarked_ideas=bookmarked_ideas)
            response_text = self._generate_llm_response(system_prompt)
            self._create_complete_synthesis_object_with_llm_response(llm_response=response_text)
        except Exception as e:
            print(
                f"[BrainstormsExecutor.generate_complete_synthesis] An error occurred while generating the complete synthesis: {e}")
            return
        print(f"[BrainstormsExecutor.generate_complete_synthesis] Complete synthesis has been generated successfully.")
        return

