#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: quick_setup_manager_views.py
#  Last Modified: 2024-11-18 20:22:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:22:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.quick_setup_helper.services import (
    action__001_organization_create,
    action__002_llm_core_create,
    action__003_meta_integration_teams_create,
    action__004_media_storages_create,
    action__005_web_browsers_create,
    action__006_ml_model_storages_create,
    action__007_memories_create,
    action__007a_orchestrator_scheduled_jobs_create,
    action__008_general_project_item_create,
    action__009_general_team_item_create,
    action__010_metakanban_board_create,
    action__011_metatempo_tracker_create,
    action__012_drafting_folder_create,
    action__013_google_docs_connections_create,
    action__014_sheetos_folder_create,
    action__015_google_sheets_connections_create,
    action__016_google_slides_connections_create,
    action__017_google_forms_connections_create,
    action__018_credit_card_create,
    action__019_balance_top_up_plan_create,
    action__020_blockchain_wallet_connection_create,
    action__021_export_assistants_create,
    action__022_export_leanmods_create,
    action__023_export_orchestrations_create,
    action__024_sql_connection_create,
    action__025_nosql_connection_create,
    action__026_knowledge_base_connection_create,
    action__027_code_base_connection_create,
    action__028_file_base_connection_create,
    action__029_invite_users_create,
    action__030_user_roles_create,
)

logger = logging.getLogger(__name__)


class QuickSetupHelperView_QuickSetupManager(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ############################################################################################################
        # STEP 1 (+10%) = 10%
        ############################################################################################################
        # Q1: What is the name of your organization?
        response__organization_name = request.POST.get('response__organization_name')

        if response__organization_name is None or response__organization_name.strip() == "":
            messages.error(request, f"Organization name is required.")
            return redirect("quick_setup_helper:wrapper")

        # Q2: Can you please describe your organization and what operations your organization is involved in?
        response__organization_description = request.POST.get('response__organization_description')

        if response__organization_description is None or response__organization_description.strip() == "":
            messages.error(request, f"Organization description is required.")
            return redirect("quick_setup_helper:wrapper")

        # Action-001: Create a new organization
        success_001, new_organization = action__001_organization_create(
            metadata__user=context_user,
            response__organization_name=response__organization_name,
            response__organization_description=response__organization_description
        )

        if success_001 is False:
            print(
                f"Failed to create a new organization. response__organization_name: {response__organization_name}")
            messages.error(request, f"Failed to create a new organization.")
            return redirect("quick_setup_helper:wrapper")
        ############################################################################################################

        ############################################################################################################
        # STEP 2 (+5%) = 15%
        ############################################################################################################
        # Q3: Please enter your OpenAI API key
        response__llm_core_openai_api_key = request.POST.get('response__llm_core_openai_api_key')

        if response__llm_core_openai_api_key is None or response__llm_core_openai_api_key.strip() == "":
            messages.error(request, f"OpenAI API key is required.")
            return redirect("quick_setup_helper:wrapper")

        # Q4: Which would be more important for your assistants? (Don't worry, you can always change you mind and update later on.)
        response__openai_temperature = request.POST.get('response__openai_temperature')

        if response__openai_temperature is None or response__openai_temperature.strip() == "":
            messages.error(request, f"Assistant behavior specifier field is required.")
            return redirect("quick_setup_helper:wrapper")

        response__openai_temperature = float(response__openai_temperature)

        # Action-002: Create the LLM Core
        success_002, new_llm_model = action__002_llm_core_create(
            metadata__user=context_user,
            metadata__organization=new_organization,
            response__llm_core_openai_api_key=response__llm_core_openai_api_key,
            response__openai_temperature=response__openai_temperature
        )

        if success_002 is False:
            print(
                f"Failed to create a new LLM Core. response__llm_core_openai_api_key.")
            messages.error(request, f"Failed to create the LLM Core.")
            return redirect("quick_setup_helper:wrapper")

        ############################################################################################################

        ############################################################################################################
        # STEP 3 (+20%) = 35%
        ############################################################################################################
        # Q5: Okay, let's hire your first team for your needs. Can you list the use cases you plan to use your AI agents?
        response__assistant_use_case_1 = request.POST.get('response__assistant_use_case_1')
        response__assistant_use_case_2 = request.POST.get('response__assistant_use_case_2')
        response__assistant_use_case_3 = request.POST.get('response__assistant_use_case_3')
        response__assistant_use_case_4 = request.POST.get('response__assistant_use_case_4')
        response__assistant_use_case_5 = request.POST.get('response__assistant_use_case_5')

        response__assistant_use_cases_list = []
        if response__assistant_use_case_1 and response__assistant_use_case_1.strip() != "":
            response__assistant_use_cases_list.append(response__assistant_use_case_1)
        if response__assistant_use_case_2 and response__assistant_use_case_2.strip() != "":
            response__assistant_use_cases_list.append(response__assistant_use_case_2)
        if response__assistant_use_case_3 and response__assistant_use_case_3.strip() != "":
            response__assistant_use_cases_list.append(response__assistant_use_case_3)
        if response__assistant_use_case_4 and response__assistant_use_case_4.strip() != "":
            response__assistant_use_cases_list.append(response__assistant_use_case_4)
        if response__assistant_use_case_5 and response__assistant_use_case_5.strip() != "":
            response__assistant_use_cases_list.append(response__assistant_use_case_5)

        if len(response__assistant_use_cases_list) != 0:

            # Action-003: Create the Meta Integration Teams
            success_003, new_assistants, new_leanmods, new_orchestrators = action__003_meta_integration_teams_create(
                metadata__user=context_user,
                metadata__organization=new_organization,
                metadata__llm_core=new_llm_model,
                response__assistant_use_cases_list=response__assistant_use_cases_list
            )

            if success_003 is False:
                print(
                    f"Failed to create the Meta Integration Teams. response__assistant_use_cases_list.")
                messages.error(request, f"Failed to create the Meta Integration Teams.")
                return redirect("quick_setup_helper:wrapper")

            if len(new_assistants) == 0:
                print(
                    f"No assistants were created. response__assistant_use_cases_list.")
                messages.error(request, f"No assistants were created.")
                return redirect("quick_setup_helper:wrapper")

            if len(new_leanmods) == 0:
                print(
                    f"No leanmods were created. response__assistant_use_cases_list.")
                messages.error(request, f"No leanmods were created.")
                return redirect("quick_setup_helper:wrapper")

            if len(new_orchestrators) == 0:
                print(
                    f"No orchestrators were created. response__assistant_use_cases_list.")
                messages.error(request, f"No orchestrators were created.")
                return redirect("quick_setup_helper:wrapper")

            # Action-004: Create the Media Storages for Assistants
            success_004 = action__004_media_storages_create(
                metadata__assistants=new_assistants
            )

            if success_004 is False:
                print(
                    f"Failed to create the Media Storages for Assistants. response__assistant_use_cases_list.")
                messages.error(request, f"Failed to create the Media Storages for Assistants.")
                pass

            # Action-005: Create the Web Browsers for Assistants
            success_005 = action__005_web_browsers_create(
                metadata__user=context_user,
                metadata__assistants=new_assistants
            )

            if success_005 is False:
                print(
                    f"Failed to create the Web Browsers for Assistants. response__assistant_use_cases_list.")
                messages.error(request, f"Failed to create the Web Browsers for Assistants.")
                pass

            # Action-006: Create the ML Model Storages for Assistants
            success_006 = action__006_ml_model_storages_create(
                metadata__assistants=new_assistants
            )

            if success_006 is False:
                print(
                    f"Failed to create the ML Model Storages for Assistants. response__assistant_use_cases_list.")
                messages.error(request, f"Failed to create the ML Model Storages for Assistants.")
                pass

        else:
            print("No assistant use cases were provided.")
            messages.error(request, f"No assistant use cases were provided.")
            return redirect("quick_setup_helper:wrapper")

        ############################################################################################################

        ############################################################################################################
        # STEP 4 (+5%) = 40%
        ############################################################################################################
        # Q6: You can list the notes you want to share with your assistants here.

        response__assistant_notes_decision = request.POST.get('response__assistant_notes_decision')

        if response__assistant_notes_decision == 'yes':

            response__assistant_note_1 = request.POST.get('response__assistant_note_1')
            response__assistant_note_2 = request.POST.get('response__assistant_note_2')
            response__assistant_note_3 = request.POST.get('response__assistant_note_3')
            response__assistant_note_4 = request.POST.get('response__assistant_note_4')
            response__assistant_note_5 = request.POST.get('response__assistant_note_5')

            response__assistant_notes = []
            if response__assistant_note_1 and response__assistant_note_1.strip() != "":
                response__assistant_notes.append(response__assistant_note_1)
            if response__assistant_note_2 and response__assistant_note_2.strip() != "":
                response__assistant_notes.append(response__assistant_note_2)
            if response__assistant_note_3 and response__assistant_note_3.strip() != "":
                response__assistant_notes.append(response__assistant_note_3)
            if response__assistant_note_4 and response__assistant_note_4.strip() != "":
                response__assistant_notes.append(response__assistant_note_4)
            if response__assistant_note_5 and response__assistant_note_5.strip() != "":
                response__assistant_notes.append(response__assistant_note_5)

            if len(response__assistant_notes) != 0:

                # Action-007: Create the memories for the assistants
                success_007 = action__007_memories_create(
                    metadata__user=context_user,
                    metadata__organization=new_organization,
                    metadata__assistants=new_assistants,
                    response__assistant_notes=response__assistant_notes
                )

                if success_007 is False:
                    print(
                        f"Failed to create the memories for the assistants. response__assistant_notes.")
                    messages.error(request, f"Failed to create the memories for the assistants.")
                    pass

            else:
                print("No assistant notes were provided, skipping.")
                pass

        elif response__assistant_notes_decision == 'no':
            print("User opt out for sharing notes with assistants, skipping.")
            pass

        else:
            print("User opt out for sharing notes with assistants, skipping.")
            pass

        ############################################################################################################

        ############################################################################################################
        # STEP 4A
        ############################################################################################################
        # Q6A. Do you want to create automated execution schedules for your assistant teams?
        response__orchestration_scheduled_jobs_decision = request.POST.get('response__assistant_scheduled_jobs_decision')

        if response__orchestration_scheduled_jobs_decision == 'yes':

            response__scheduled_job_interval = request.POST.get('response__scheduled_job_interval')
            response__scheduled_job_description = request.POST.get('response__scheduled_job_description')

            if (
                response__scheduled_job_interval and response__scheduled_job_interval.strip() != "" and
                response__scheduled_job_description and response__scheduled_job_description.strip() != ""
            ):

                response__scheduled_job_step_1 = request.POST.get('response__scheduled_job_step_1')
                response__scheduled_job_step_2 = request.POST.get('response__scheduled_job_step_2')
                response__scheduled_job_step_3 = request.POST.get('response__scheduled_job_step_3')
                response__scheduled_job_step_4 = request.POST.get('response__scheduled_job_step_4')
                response__scheduled_job_step_5 = request.POST.get('response__scheduled_job_step_5')

                response__scheduled_job_step_guides = []
                if response__scheduled_job_step_1 and response__scheduled_job_step_1.strip() != "":
                    response__scheduled_job_step_guides.append(response__scheduled_job_step_1)
                if response__scheduled_job_step_2 and response__scheduled_job_step_2.strip() != "":
                    response__scheduled_job_step_guides.append(response__scheduled_job_step_2)
                if response__scheduled_job_step_3 and response__scheduled_job_step_3.strip() != "":
                    response__scheduled_job_step_guides.append(response__scheduled_job_step_3)
                if response__scheduled_job_step_4 and response__scheduled_job_step_4.strip() != "":
                    response__scheduled_job_step_guides.append(response__scheduled_job_step_4)
                if response__scheduled_job_step_5 and response__scheduled_job_step_5.strip() != "":
                    response__scheduled_job_step_guides.append(response__scheduled_job_step_5)

                if len(response__scheduled_job_step_guides) != 0:

                    success_007a = action__007a_orchestrator_scheduled_jobs_create(
                        metadata__user=context_user,
                        response__scheduled_job_description=response__scheduled_job_description,
                        response__scheduled_job_interval=response__scheduled_job_interval,
                        response__scheduled_job_step_guides=response__scheduled_job_step_guides,
                        metadata__orchestrators=new_orchestrators
                    )

                    if success_007a is False:
                        print(
                            f"Failed to create the scheduled jobs for the orchestrators.")
                        messages.error(request, f"Failed to create the scheduled jobs for the orchestrators.")
                        pass

                else:
                    messages.error(request, f"Please provide at least '1 (one)' step of process description for the scheduled job, if you are going to create any.")
                    return redirect("quick_setup_helper:wrapper")

            else:
                print("No scheduled job interval, description, or steps were provided, skipping.")
                pass

        elif response__orchestration_scheduled_jobs_decision == 'no':
            print("User opt out for creating automated execution schedules for assistant teams, skipping.")
            pass

        else:
            print("User opt out for creating automated execution schedules for assistant teams, skipping.")
            pass

        ############################################################################################################
        # STEP 5 (+10%) = 50%
        ############################################################################################################
        # Q7: Do you plan to use BimodLab AI Office tools & applications (e.g. Drafting, Spreadsheets, Slides, Forms, Kanban management, and Tempo Tracking)?
        response__bimodlab_tools_decision = request.POST.get('response__bimodlab_tools_decision')
        if response__bimodlab_tools_decision == 'yes':

            # Action-008: Create the General Project Item
            success_008, new_project_item = action__008_general_project_item_create(
                metadata__user=context_user,
                metadata__organization=new_organization,
                metadata__assistants=new_assistants
            )

            if success_008 is False:
                print(
                    f"Failed to create the General Project Item.")
                messages.error(request, f"Failed to create the General Project Item.")
                pass

            if new_project_item:

                # Action-009: Create the General Team Item
                success_009, new_team_item = action__009_general_team_item_create(
                    metadata__user=context_user,
                    metadata__project_item=new_project_item
                )

                if success_009 is False:
                    print(
                        f"Failed to create the General Team Item.")
                    messages.error(request, f"Failed to create the General Team Item.")
                    pass

                # Action-010: Create a MetaKanban Board
                success_010, new_metakanban_board = action__010_metakanban_board_create(
                    metadata__user=context_user,
                    metadata__organization=new_organization,
                    metadata__llm_core=new_llm_model,
                    metadata__assistants=new_assistants,
                    metadata__project=new_project_item
                )

                if success_010 is False:
                    print(
                        f"Failed to create the MetaKanban Board.")
                    messages.error(request, f"Failed to create the MetaKanban Board.")
                    pass

                if new_metakanban_board:

                    # Action-011: Create a MetaTempo Tracker
                    success_011, new_metatempo_item = action__011_metatempo_tracker_create(
                        metadata__user=context_user,
                        metadata__metakanban_board=new_metakanban_board,
                        metadata__assistants=new_assistants
                    )

                    if success_011 is False:
                        print(
                            f"Failed to create the MetaTempo Tracker.")
                        messages.error(request, f"Failed to create the MetaTempo Tracker.")
                        pass

                else:
                    print("Failed to create the MetaKanban Board, skipping.")
                    pass

            else:
                print("Failed to create the General Project Item, skipping.")
                pass

            # Action-012: Create a Drafting Folder
            success_012, new_drafting_folder = action__012_drafting_folder_create(
                metadata__user=context_user,
                metadata__organization=new_organization
            )

            if success_012 is False:
                print(
                    f"Failed to create the Drafting Folder.")
                messages.error(request, f"Failed to create the Drafting Folder.")
                pass

            # Action-013: Create Google Docs Connections for Each Assistant
            success_013 = action__013_google_docs_connections_create(
                metadata__user=context_user,
                metadata__assistants=new_assistants
            )

            if success_013 is False:
                print(
                    f"Failed to create the Google Docs Connections for Each Assistant.")
                messages.error(request, f"Failed to create the Google Docs Connections for Each Assistant.")
                pass

            # Action-014: Create a Sheetos Folder
            success_014, new_sheetos_folder = action__014_sheetos_folder_create(
                metadata__user=context_user,
                metadata__organization=new_organization,
            )

            if success_014 is False:
                print(
                    f"Failed to create the Sheetos Folder.")
                messages.error(request, f"Failed to create the Sheetos Folder.")
                pass

            # Action-015: Create Google Sheets Connections for Each Assistant
            success_015 = action__015_google_sheets_connections_create(
                metadata__user=context_user,
                metadata__assistants=new_assistants
            )

            if success_015 is False:
                print(
                    f"Failed to create the Google Sheets Connections for Each Assistant.")
                messages.error(request, f"Failed to create the Google Sheets Connections for Each Assistant.")
                pass

            # Action-016: Create Google Slides Connections for Each Assistant
            success_016 = action__016_google_slides_connections_create(
                metadata__user=context_user,
                metadata__assistants=new_assistants
            )

            if success_016 is False:
                print(
                    f"Failed to create the Google Slides Connections for Each Assistant.")
                messages.error(request, f"Failed to create the Google Slides Connections for Each Assistant.")
                pass

            # Action-017: Create Google Forms Connections for Each Assistant
            success_017 = action__017_google_forms_connections_create(
                metadata__user=context_user,
                metadata__assistants=new_assistants
            )

            if success_017 is False:
                print(
                    f"Failed to create the Google Forms Connections for Each Assistant.")
                messages.error(request, f"Failed to create the Google Forms Connections for Each Assistant.")
                pass

        elif response__bimodlab_tools_decision == 'no':
            print("User opt out for using BimodLab AI Office tools & applications, skipping.")
            pass

        else:
            print("User opt out for using BimodLab AI Office tools & applications, skipping.")
            pass
        ############################################################################################################

        ############################################################################################################
        # STEP 6 (+5%) = 55%
        ############################################################################################################

        # Q-i1: Do you want to add a payment method to your account now?
        if request.POST.get('response__payment_method_decision') == 'yes':

            # Q8: Please fill in the form here to add a new credit card
            response__payment_method_credit_card_name = request.POST.get('response__payment_method_credit_card_name')
            response__payment_method_credit_card_number = request.POST.get(
                'response__payment_method_credit_card_number')
            response__payment_method_credit_card_expiration_month = request.POST.get(
                'response__payment_method_credit_card_expiration_month')
            response__payment_method_credit_card_expiration_year = request.POST.get(
                'response__payment_method_credit_card_expiration_year')
            response__payment_method_credit_card_cvc = request.POST.get('response__payment_method_credit_card_cvc')

            # Action-018: Create a new credit card
            if (
                response__payment_method_credit_card_name and response__payment_method_credit_card_name.strip() != "" and
                response__payment_method_credit_card_number and response__payment_method_credit_card_number.strip() != "" and
                response__payment_method_credit_card_expiration_month and response__payment_method_credit_card_expiration_month.strip() != "" and
                response__payment_method_credit_card_expiration_year and response__payment_method_credit_card_expiration_year.strip() != "" and
                response__payment_method_credit_card_cvc and response__payment_method_credit_card_cvc.strip() != ""
            ):
                success_018, new_payment_method = action__018_credit_card_create(
                    metadata__user=context_user,
                    response__payment_method_credit_card_name=response__payment_method_credit_card_name,
                    response__payment_method_credit_card_number=response__payment_method_credit_card_number,
                    response__payment_method_credit_card_expiration_month=response__payment_method_credit_card_expiration_month,
                    response__payment_method_credit_card_expiration_year=response__payment_method_credit_card_expiration_year,
                    response__payment_method_credit_card_cvc=response__payment_method_credit_card_cvc
                )

                if success_018 is False:
                    print(
                        f"Failed to create a new credit card.")
                    messages.error(request, f"Failed to create a new credit card.")
                    pass

            else:
                print("User opt out for adding a new credit card, skipping.")
                pass

        elif request.POST.get('response__payment_method_decision') == 'no':
            print("User opt out for adding a new credit card, skipping.")
            pass

        else:
            print("User opt out for adding a new credit card, skipping.")
            pass

        ############################################################################################################

        ############################################################################################################
        # STEP 7 (+5%) = 60%
        ############################################################################################################
        # Q9: Do you want to create an automated balance top-up plan to prevent any service interruptions?
        response__balance_top_up_decision = request.POST.get('response__balance_top_up_decision')
        if response__balance_top_up_decision == 'yes':

            # Q10: Which one seem to be a better option for you to top up your balance?
            response__balance_top_up_option = request.POST.get('response__balance_top_up_option')
            response__balance_top_up_amount = request.POST.get('response__balance_top_up_amount')

            if response__balance_top_up_option is None or response__balance_top_up_option.strip() == "":
                messages.error(request, f"Balance top-up option is required since you opt for automated balance top-up creation.")
                return redirect("quick_setup_helper:wrapper")

            if response__balance_top_up_amount is None or response__balance_top_up_amount.strip() == "":
                messages.error(request, f"Balance top-up amount is required since you opt for automated balance top-up creation.")
                return redirect("quick_setup_helper:wrapper")

            response__balance_top_up_interval_days = None
            response__balance_top_up_threshold_value = None
            response__balance_top_up_hard_limit = None

            if response__balance_top_up_option == 'regular_interval':

                # Q11-A: How often do you want your balance to be topped, and by how much? Also, please set up a monthly top-up hard limit.
                response__balance_top_up_interval_days = request.POST.get('response__balance_top_up_interval_days')
                response__balance_top_up_hard_limit = request.POST.get('response__balance_top_up_hard_limit')

                if response__balance_top_up_interval_days is None or response__balance_top_up_interval_days.strip() == "":
                    messages.error(request, f"Balance top-up interval days is required since you opt for automated balance top-up creation.")
                    return redirect("quick_setup_helper:wrapper")

                if response__balance_top_up_hard_limit is None or response__balance_top_up_hard_limit.strip() == "":
                    messages.error(request, f"Balance top-up hard limit is required since you opt for automated balance top-up creation.")
                    return redirect("quick_setup_helper:wrapper")

            elif response__balance_top_up_option == 'threshold_trigger':

                # Q11-B: What should be the balance threshold value to trigger the top-up, and by how much should the balance be topped up? Also, please set up a monthly top-up hard limit.
                response__balance_top_up_threshold_value = request.POST.get('response__balance_top_up_threshold_value')
                response__balance_top_up_hard_limit = request.POST.get('response__balance_top_up_hard_limit')

                if response__balance_top_up_threshold_value is None or response__balance_top_up_threshold_value.strip() == "":
                    messages.error(request, f"Balance top-up threshold value is required since you opt for automated balance top-up creation.")
                    return redirect("quick_setup_helper:wrapper")

                if response__balance_top_up_hard_limit is None or response__balance_top_up_hard_limit.strip() == "":
                    messages.error(request, f"Balance top-up hard limit is required since you opt for automated balance top-up creation.")
                    return redirect("quick_setup_helper:wrapper")

            else:
                print("User opt out for creating an automated balance top-up plan, skipping.")
                pass

            # Action-019: Create an automated balance top-up plan
            success_019, new_top_up_plan = action__019_balance_top_up_plan_create(
                metadata__user=context_user,
                metadata__organization=new_organization,
                option=response__balance_top_up_option,
                response__balance_top_up_amount=response__balance_top_up_amount,
                response__balance_top_up_interval_days=response__balance_top_up_interval_days,
                response__balance_top_up_threshold_value=response__balance_top_up_threshold_value,
                response__balance_top_up_hard_limit=response__balance_top_up_hard_limit
            )

            if success_019 is False:
                print(
                    f"Failed to create an automated balance top-up plan.")
                messages.error(request, f"Failed to create an automated balance top-up plan.")
                pass

        elif response__balance_top_up_decision == 'no':
            print("User opt out for creating an automated balance top-up plan, skipping.")
            pass

        else:
            print("User opt out for creating an automated balance top-up plan, skipping.")
            pass
        ############################################################################################################

        ############################################################################################################
        # STEP 8 (+5%) = 65%
        ############################################################################################################
        # Q12: Do you want to connect your Blockchain wallet to let your assistants manage & create smart contracts?
        response__blockchain_wallet_decision = request.POST.get('response__blockchain_wallet_decision')
        if response__blockchain_wallet_decision == 'yes':

            # Q13: Please enter your Ethereum wallet address and private key below.
            response__blockchain_wallet_address = request.POST.get('response__blockchain_wallet_address')
            response__blockchain_wallet_private_key = request.POST.get('response__blockchain_wallet_private_key')

            if (
                response__blockchain_wallet_address and response__blockchain_wallet_address.strip() != "" and
                response__blockchain_wallet_private_key and response__blockchain_wallet_private_key.strip() != ""
            ):

                # Action-020: Create a new blockchain wallet connection
                success_020, new_wallet_connection = action__020_blockchain_wallet_connection_create(
                    metadata__user=context_user,
                    metadata__organization=new_organization,
                    response__blockchain_wallet_address=response__blockchain_wallet_address,
                    response__blockchain_wallet_private_key=response__blockchain_wallet_private_key
                )

                if success_020 is False:
                    print(
                        f"Failed to create a new blockchain wallet connection.")
                    messages.error(request, f"Failed to create a new blockchain wallet connection.")
                    pass

            else:
                print("User opt out for connecting a blockchain wallet, skipping.")
                pass

        elif response__blockchain_wallet_decision == 'no':
            print("User opt out for connecting a blockchain wallet, skipping.")
            pass

        else:
            print("User opt out for connecting a blockchain wallet, skipping.")
            pass

        ############################################################################################################

        ############################################################################################################
        # STEP 9 (+10%) = 75%
        ############################################################################################################
        # Q14: Do you plan to use your assistants externally (e.g. in your own website, applications, or platforms)?
        response__external_usage_decision = request.POST.get('response__external_usage_decision')

        if response__external_usage_decision == 'yes':

            # Action-021: Create export Assistants for created Assistants
            success_021 = action__021_export_assistants_create(
                metadata__user=context_user,
                metadata__organization=new_organization,
                metadata__assistants=new_assistants
            )

            if success_021 is False:
                print(
                    f"Failed to create export Assistants for created Assistants.")
                messages.error(request, f"Failed to create export Assistants for created Assistants.")
                pass

            # Action-022: Create export LeanMods for created LeanMods
            success_022 = action__022_export_leanmods_create(
                metadata__user=context_user,
                metadata__organization=new_organization,
                metadata__leanmods=new_leanmods
            )

            if success_022 is False:
                print(
                    f"Failed to create export LeanMods for created LeanMods.")
                messages.error(request, f"Failed to create export LeanMods for created LeanMods.")
                pass

            # Action-023: Create export Orchestrations for created Orchestrations
            success_023 = action__023_export_orchestrations_create(
                metadata__user=context_user,
                metadata__organization=new_organization,
                metadata__orchestrators=new_orchestrators
            )

            if success_023 is False:
                print(
                    f"Failed to create export Orchestrations for created Orchestrations.")
                messages.error(request, f"Failed to create export Orchestrations for created Orchestrations.")
                pass

        elif response__external_usage_decision == 'no':
            print("User opt out for using assistants externally, skipping.")
            pass

        else:
            print("User opt out for using assistants externally, skipping.")
            pass
        ############################################################################################################

        ############################################################################################################
        # STEP 10 (+15%) = 90%
        ############################################################################################################
        # Q15: Do you want to integrate your internal data sources (e.g. SQL/NoSQL databases, Text Documents such as pdf, txt, docx, xlsx, etc., GitHub Code Repositories, Servers/Computers) now?
        response__internal_data_sources_decision = request.POST.get('response__internal_data_sources_decision')
        if response__internal_data_sources_decision == 'yes':

            # Q16: Please fill in the relevant fields of this form to connect your internal data sources.

            #       - (0) For all of them
            response__internal_data_sources__data_source_is_read_only = request.POST.get(
                'response__internal_data_sources__data_source_is_read_only')

            if response__internal_data_sources__data_source_is_read_only is None or response__internal_data_sources__data_source_is_read_only.strip() == "":
                messages.error(request, f"Data source read-only specifier field is required since you opt for connecting internal data sources.")
                return redirect("quick_setup_helper:wrapper")

            if response__internal_data_sources__data_source_is_read_only == 'yes':
                is_read_only_bool_value = True
            elif response__internal_data_sources__data_source_is_read_only == 'no':
                is_read_only_bool_value = False
            else:
                is_read_only_bool_value = True

            #       - (1) Answers for @ SQL
            response__internal_data_sources__sql_dbms_type = request.POST.get(
                'response__internal_data_sources__sql_dbms_type')
            response__internal_data_sources__sql_host = request.POST.get('response__internal_data_sources__sql_host')
            response__internal_data_sources__sql_port = request.POST.get('response__internal_data_sources__sql_port')
            response__internal_data_sources__sql_database_name = request.POST.get(
                'response__internal_data_sources__sql_database_name')
            response__internal_data_sources__sql_username = request.POST.get(
                'response__internal_data_sources__sql_username')
            response__internal_data_sources__sql_password = request.POST.get(
                'response__internal_data_sources__sql_password')

            required_fields__data_sources__sql = [
                response__internal_data_sources__sql_dbms_type,
                response__internal_data_sources__sql_host,
                response__internal_data_sources__sql_port,
                response__internal_data_sources__sql_database_name,
                response__internal_data_sources__sql_username,
                response__internal_data_sources__sql_password,
            ]

            if all(field and field.strip() != "" for field in required_fields__data_sources__sql):
                # Action-024: Create a new SQL connection
                success_024 = action__024_sql_connection_create(
                    metadata__user=context_user,
                    metadata__organization=new_organization,
                    metadata__assistants=new_assistants,
                    response__internal_data_sources__sql_dbms_type=response__internal_data_sources__sql_dbms_type,
                    response__internal_data_sources__sql_host=response__internal_data_sources__sql_host,
                    response__internal_data_sources__sql_port=response__internal_data_sources__sql_port,
                    response__internal_data_sources__sql_database_name=response__internal_data_sources__sql_database_name,
                    response__internal_data_sources__sql_username=response__internal_data_sources__sql_username,
                    response__internal_data_sources__sql_password=response__internal_data_sources__sql_password,
                    is_read_only=is_read_only_bool_value
                )

                if success_024 is False:
                    print(
                        f"Failed to create a new SQL connection.")
                    messages.error(request, f"Failed to create a new SQL connection.")
                    pass
            else:
                print("User opt out for adding a new SQL connection.")
                pass

            #       - (2) Answers for @ NoSQL
            response__internal_data_sources__nosql_db_type = request.POST.get(
                'response__internal_data_sources__nosql_db_type')
            response__internal_data_sources__nosql_host = request.POST.get(
                'response__internal_data_sources__nosql_host')
            response__internal_data_sources__nosql_bucket_name = request.POST.get(
                'response__internal_data_sources__nosql_bucket_name')
            response__internal_data_sources__nosql_username = request.POST.get(
                'response__internal_data_sources__nosql_username')
            response__internal_data_sources__nosql_password = request.POST.get(
                'response__internal_data_sources__nosql_password')

            required_fields__data_sources__nosql = [
                response__internal_data_sources__nosql_db_type,
                response__internal_data_sources__nosql_host,
                response__internal_data_sources__nosql_bucket_name,
                response__internal_data_sources__nosql_username,
                response__internal_data_sources__nosql_password,
            ]

            if all(field and field.strip() != "" for field in required_fields__data_sources__nosql):

                # Action-025: Create a new NoSQL connection
                success_025 = action__025_nosql_connection_create(
                    metadata__user=context_user,
                    metadata__organization=new_organization,
                    metadata__assistants=new_assistants,
                    response__internal_data_sources__nosql_db_type=response__internal_data_sources__nosql_db_type,
                    response__internal_data_sources__nosql_host=response__internal_data_sources__nosql_host,
                    response__internal_data_sources__nosql_bucket_name=response__internal_data_sources__nosql_bucket_name,
                    response__internal_data_sources__nosql_username=response__internal_data_sources__nosql_username,
                    response__internal_data_sources__nosql_password=response__internal_data_sources__nosql_password,
                    is_read_only=is_read_only_bool_value
                )

                if success_025 is False:
                    print(
                        f"Failed to create a new NoSQL connection.")
                    messages.error(request, f"Failed to create a new NoSQL connection.")
                    pass
            else:
                print("User opt out for adding a new NoSQL connection.")
                pass

            #       - (3) Answers for @ Knowledge Base
            response__internal_data_sources__knowledge_base_provider = request.POST.get(
                'response__internal_data_sources__knowledge_base_provider')
            response__internal_data_sources__knowledge_base_host_url = request.POST.get(
                'response__internal_data_sources__knowledge_base_host_url')
            response__internal_data_sources__knowledge_base_provider_api_key = request.POST.get(
                'response__internal_data_sources__knowledge_base_provider_api_key')

            required_fields__data_sources__knowledge_base = [
                response__internal_data_sources__knowledge_base_provider,
                response__internal_data_sources__knowledge_base_host_url,
                response__internal_data_sources__knowledge_base_provider_api_key,
            ]

            if all(field and field.strip() != "" for field in required_fields__data_sources__knowledge_base):

                # Action-026: Create a new Knowledge Base connection
                success_026 = action__026_knowledge_base_connection_create(
                    metadata__organization=new_organization,
                    metadata__llm_core=new_llm_model,
                    metadata__assistants=new_assistants,
                    response__internal_data_sources__knowledge_base_provider=response__internal_data_sources__knowledge_base_provider,
                    response__internal_data_sources__knowledge_base_host_url=response__internal_data_sources__knowledge_base_host_url,
                    response__internal_data_sources__knowledge_base_provider_api_key=response__internal_data_sources__knowledge_base_provider_api_key
                )

                if success_026 is False:
                    print(
                        f"Failed to create a new Knowledge Base connection.")
                    messages.error(request, f"Failed to create a new Knowledge Base connection.")
                    pass
            else:
                print("User opt out for adding a new Knowledge Base connection.")
                pass

            #       - (4) Answers for @ Code Base
            response__internal_data_sources__code_base_provider = request.POST.get(
                'response__internal_data_sources__code_base_provider')
            response__internal_data_sources__code_base_host_url = request.POST.get(
                'response__internal_data_sources__code_base_host_url')
            response__internal_data_sources__code_base_provider_api_key = request.POST.get(
                'response__internal_data_sources__code_base_provider_api_key')

            required_fields__data_sources__code_base = [
                response__internal_data_sources__code_base_provider,
                response__internal_data_sources__code_base_host_url,
                response__internal_data_sources__code_base_provider_api_key,
            ]

            if all(field and field.strip() != "" for field in required_fields__data_sources__code_base):

                # Action-027: Create a new Code Base connection
                success_027 = action__027_code_base_connection_create(
                    metadata__organization=new_organization,
                    metadata__llm_core=new_llm_model,
                    metadata__assistants=new_assistants,
                    response__internal_data_sources__code_base_provider=response__internal_data_sources__code_base_provider,
                    response__internal_data_sources__code_base_host_url=response__internal_data_sources__code_base_host_url,
                    response__internal_data_sources__code_base_provider_api_key=response__internal_data_sources__code_base_provider_api_key
                )

                if success_027 is False:
                    print(
                        f"Failed to create a new Code Base connection.")
                    messages.error(request, f"Failed to create a new Code Base connection.")
                    pass
            else:
                print("User opt out for adding a new Code Base connection.")
                pass

            #       - (5) Answers for @ File Base (SSH)
            response__internal_data_sources__file_base_os_type = request.POST.get(
                'response__internal_data_sources__file_base_os_type')
            response__internal_data_sources__file_base_host_url = request.POST.get(
                'response__internal_data_sources__file_base_host_url')
            response__internal_data_sources__file_base_port = request.POST.get(
                'response__internal_data_sources__file_base_port')
            response__internal_data_sources__file_base_username = request.POST.get(
                'response__internal_data_sources__file_base_username')
            response__internal_data_sources__file_base_password = request.POST.get(
                'response__internal_data_sources__file_base_password')

            required_fields__data_sources__file_base = [
                response__internal_data_sources__file_base_os_type,
                response__internal_data_sources__file_base_host_url,
                response__internal_data_sources__file_base_port,
                response__internal_data_sources__file_base_username,
                response__internal_data_sources__file_base_password,
            ]

            if all(field and field.strip() != "" for field in required_fields__data_sources__file_base):

                # Action-028: Create a new File Base connection
                success_028 = action__028_file_base_connection_create(
                    metadata__user=context_user,
                    metadata__organization=new_organization,
                    metadata__assistants=new_assistants,
                    response__internal_data_sources__file_base_os_type=response__internal_data_sources__file_base_os_type,
                    response__internal_data_sources__file_base_host_url=response__internal_data_sources__file_base_host_url,
                    response__internal_data_sources__file_base_port=response__internal_data_sources__file_base_port,
                    response__internal_data_sources__file_base_username=response__internal_data_sources__file_base_username,
                    response__internal_data_sources__file_base_password=response__internal_data_sources__file_base_password,
                    is_read_only=is_read_only_bool_value
                )

                if success_028 is False:
                    print(
                        f"Failed to create a new File Base connection.")
                    messages.error(request, f"Failed to create a new File Base connection.")
                    pass

            else:
                print("User opt out for adding a new File Base connection.")
                pass

        elif response__internal_data_sources_decision == 'no':
            print("User opt out for connecting internal data sources.")
            pass

        else:
            print("User opt out for connecting internal data sources.")
            pass
        ############################################################################################################

        ############################################################################################################
        # STEP 11 (+5%) = 95%
        ############################################################################################################
        # Q17: Do you want to invite users to your organization?
        response__invite_users_decision = request.POST.get('response__invite_users_decision')
        invited_new_users = []
        if response__invite_users_decision == 'yes':

            # Q18: Please enter the email addresses of the users you want to invite to your organization.
            response__invite_users_email_address_1 = request.POST.get('response__invite_users_email_address_1')
            response__invite_users_email_address_2 = request.POST.get('response__invite_users_email_address_2')
            response__invite_users_email_address_3 = request.POST.get('response__invite_users_email_address_3')
            response__invite_users_email_address_4 = request.POST.get('response__invite_users_email_address_4')
            response__invite_users_email_address_5 = request.POST.get('response__invite_users_email_address_5')

            response__invite_users_email_addresses = []
            if response__invite_users_email_address_1 and response__invite_users_email_address_1.strip() != "":
                response__invite_users_email_addresses.append(response__invite_users_email_address_1)
            if response__invite_users_email_address_2 and response__invite_users_email_address_2.strip() != "":
                response__invite_users_email_addresses.append(response__invite_users_email_address_2)
            if response__invite_users_email_address_3 and response__invite_users_email_address_3.strip() != "":
                response__invite_users_email_addresses.append(response__invite_users_email_address_3)
            if response__invite_users_email_address_4 and response__invite_users_email_address_4.strip() != "":
                response__invite_users_email_addresses.append(response__invite_users_email_address_4)
            if response__invite_users_email_address_5 and response__invite_users_email_address_5.strip() != "":
                response__invite_users_email_addresses.append(response__invite_users_email_address_5)

            if len(response__invite_users_email_addresses) != 0:

                # Action-029: Add users and their profiles to the organization and application
                success_029, invited_new_users = action__029_invite_users_create(
                    metadata__user=context_user,
                    metadata__organization=new_organization,
                    response__invite_users_email_addresses=response__invite_users_email_addresses
                )

                if success_029 is False:
                    print(
                        f"Failed to add users and their profiles to the organization and application.")
                    messages.error(request, f"Failed to add users and their profiles to the organization and application.")
                    pass

            else:
                print("User opt out for inviting users to the organization.")
                pass

        elif response__invite_users_decision == 'no':
            print("User opt out for inviting users to the organization.")
            pass

        else:
            print("User opt out for inviting users to the organization.")
            pass
        ############################################################################################################

        ############################################################################################################
        # STEP 12 (+5%) = 100%
        ############################################################################################################

        if response__invite_users_decision == 'yes' and invited_new_users is not None and len(invited_new_users) > 0:

            # Q19: As the final step, do you want to adjust the permissions / user roles for your users?
            response__user_roles_decision = request.POST.get('response__user_roles_decision')

            if response__user_roles_decision == 'yes':

                # Q20: Which of the following options would work best for your requirements regarding user permissions?
                response__user_roles_option = request.POST.get('response__user_roles_option')
                if response__user_roles_option and response__user_roles_option in ['full_access', 'moderation_access', 'limited_access']:

                    # Action-030: Create new user roles
                    success_030 = action__030_user_roles_create(
                        metadata__user=context_user,
                        metadata__organization=new_organization,
                        metadata__invited_new_users=invited_new_users,
                        response__user_roles_option=response__user_roles_option
                    )

                    if success_030 is False:
                        print(
                            f"Failed to create new user roles.")
                        messages.error(request, f"Failed to create new user roles.")
                        pass

                else:
                    print("User opt out for adjusting the permissions / user roles for the users.")
                    pass

            else:
                print("User opt out for adjusting the permissions / user roles for the users.")
                return redirect("multimodal_chat:main_workspace")
            ############################################################################################################

            # Redirect-2: Redirect to the workspace
            print("Finished the setup successfully with user role additions. Redirecting to the workspace hub.")
            return redirect("multimodal_chat:main_workspace")

        else:

            # Redirect-2: Redirect to the workspace
            print("Finished the setup without user invitations. Redirecting to the workspace hub.")
            return redirect("multimodal_chat:main_workspace")

        ############################################################################################################
