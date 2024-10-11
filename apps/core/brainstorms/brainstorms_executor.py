#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: brainstorms_executor.py
#  Last Modified: 2024-10-05 02:13:33
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


from openai import OpenAI

from apps.core.brainstorms.utils import build_from_scratch_brainstorms_system_prompt, find_json_presence, \
    build_from_previous_level_brainstorms_system_prompt, build_synthesis_from_level_system_prompt, \
    build_synthesis_from_all_levels_system_prompt, build_deepen_thought_over_idea_system_prompt
from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
from apps.brainstorms.models import BrainstormingIdea
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


class BrainstormsExecutor:
    from apps.brainstorms.models import BrainstormingSession

    def __init__(self, session: BrainstormingSession):
        self.session = session
        self.client = OpenAI(api_key=self.session.llm_model.api_key)

    def _generate_llm_response(self, system_prompt: str):
        from apps.core.generative_ai.utils import ChatRoles
        system_message = {"role": ChatRoles.SYSTEM.lower(), "content": system_prompt}

        LLMTransaction.objects.create(
            organization=self.session.organization, model=self.session.llm_model,
            responsible_user=self.session.created_by_user, responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=system_prompt,
            llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
            transaction_type=ChatRoles.SYSTEM, transaction_source=LLMTransactionSourcesTypesNames.BRAINSTORMING,
        )

        choice_message_content = None
        try:
            llm_response = self.client.chat.completions.create(
                model=self.session.llm_model.model_name, messages=[system_message],
                temperature=float(self.session.llm_model.temperature),
                frequency_penalty=float(self.session.llm_model.frequency_penalty),
                presence_penalty=float(self.session.llm_model.presence_penalty),
                max_tokens=int(self.session.llm_model.maximum_tokens), top_p=float(self.session.llm_model.top_p),
            )
            choices = llm_response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
        except Exception as e:
            pass
        output = choice_message_content
        return output

    def _deepen_idea_object_with_llm_response(self, idea: BrainstormingIdea, llm_response: str):
        elements = []
        try:
            elements = find_json_presence(response=llm_response)
        except Exception as e:
            pass

        element = elements[0]
        try:
            existing_idea = BrainstormingIdea.objects.get(id=idea.id)
            if not existing_idea:
                return
            existing_idea.idea_description = element.get("deep_description")
            existing_idea.save()
        except Exception as e:
            return
        return


    def _create_idea_objects_with_llm_response(self, llm_response: str, depth_level: int):
        from apps.brainstorms.models import BrainstormingIdea
        elements = []
        try:
            elements = find_json_presence(response=llm_response)
        except Exception as e:
            pass

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
                continue
        return

    def _create_level_synthesis_object_with_llm_response(self, llm_response: str, depth_level: int):
        from apps.brainstorms.models import BrainstormingLevelSynthesis
        try:
            element = find_json_presence(response=llm_response)[0]
        except Exception as e:
            return

        try:
            session = self.session
            created_by_user = session.created_by_user
            synthesis_content = element.get("synthesis_content")
            BrainstormingLevelSynthesis.objects.create(
                brainstorming_session=session, created_by_user=created_by_user, synthesis_content=synthesis_content,
                depth_level=depth_level)
        except Exception as e:
            return
        return

    def _create_complete_synthesis_object_with_llm_response(self, llm_response: str):
        from apps.brainstorms.models import BrainstormingCompleteSynthesis
        try:
            element = find_json_presence(response=llm_response)[0]
        except Exception as e:
            return

        try:
            session = self.session
            created_by_user = session.created_by_user
            synthesis_content = element.get("synthesis_content")
            BrainstormingCompleteSynthesis.objects.create(
                brainstorming_session=session, created_by_user=created_by_user, synthesis_content=synthesis_content)
        except Exception as e:
            return
        return

    #################################################################################################################

    def produce_ideas(self, depth_level=1):
        from apps.brainstorms.models import BrainstormingIdea
        try:
            if depth_level == 1:
                system_prompt = build_from_scratch_brainstorms_system_prompt(session=self.session)
                output = self._generate_llm_response(system_prompt)
                self._create_idea_objects_with_llm_response(llm_response=output, depth_level=depth_level)
            else:
                previous_depth_level = (depth_level - 1)
                previous_level_bookmarked_ideas = BrainstormingIdea.objects.filter(
                    brainstorming_session=self.session, depth_level=previous_depth_level, is_bookmarked=True)
                system_prompt = build_from_previous_level_brainstorms_system_prompt(
                    session=self.session, previous_level_bookmarked_ideas=previous_level_bookmarked_ideas)
                output = self._generate_llm_response(system_prompt)
                self._create_idea_objects_with_llm_response(llm_response=output, depth_level=depth_level)
        except Exception as e:
            return
        return

    def generate_level_synthesis(self, depth_level):
        from apps.brainstorms.models import BrainstormingIdea, BrainstormingLevelSynthesis
        try:
            existing_syntheses = BrainstormingLevelSynthesis.objects.filter(
                brainstorming_session=self.session, depth_level=depth_level)
            if existing_syntheses.exists():
                existing_syntheses.delete()

            depth_level_bookmarked_ideas = BrainstormingIdea.objects.filter(
                brainstorming_session=self.session, depth_level=depth_level, is_bookmarked=True)
            system_prompt = build_synthesis_from_level_system_prompt(
                session=self.session, bookmarked_ideas=depth_level_bookmarked_ideas)
            output = self._generate_llm_response(system_prompt)
            self._create_level_synthesis_object_with_llm_response(llm_response=output, depth_level=depth_level)
        except Exception as e:
            return
        return

    def generate_complete_synthesis(self):
        from apps.brainstorms.models import BrainstormingIdea, BrainstormingCompleteSynthesis
        try:
            existing_syntheses = BrainstormingCompleteSynthesis.objects.filter(brainstorming_session=self.session)
            if existing_syntheses.exists():
                existing_syntheses.delete()

            bookmarked_ideas = BrainstormingIdea.objects.filter(
                brainstorming_session=self.session, is_bookmarked=True)
            system_prompt = build_synthesis_from_all_levels_system_prompt(
                session=self.session, bookmarked_ideas=bookmarked_ideas)
            output = self._generate_llm_response(system_prompt)
            self._create_complete_synthesis_object_with_llm_response(llm_response=output)
        except Exception as e:
            return
        return

    def deepen_thought_over_idea(self, idea: BrainstormingIdea):
        try:
            system_prompt = build_deepen_thought_over_idea_system_prompt(idea=idea)
            output = self._generate_llm_response(system_prompt)
            self._deepen_idea_object_with_llm_response(idea=idea, llm_response=output)
        except Exception as e:
            return
        return

