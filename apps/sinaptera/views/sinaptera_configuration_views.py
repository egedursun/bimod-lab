#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sinaptera_configuration_views.py
#  Last Modified: 2024-12-16 18:58:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-16 18:58:22
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json
import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.shortcuts import redirect

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.sinaptera.models import (
    SinapteraConfiguration
)

from apps.sinaptera.utils import (
    estimate_sinaptera_cost_multiplier,
    estimate_sinaptera_speed_percentage,
    estimate_sinaptera_accuracy)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SinapteraView_Configuration(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - USE_SINAPTERA_CONFIGURATION
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.USE_SINAPTERA_CONFIGURATION
        ):
            messages.error(
                self.request,
                "You do not have permission to create and use Sinaptera configurations."
            )

            logger.error(
                f"User {self.request.user} does not have permission to create and use Sinaptera configurations."
            )

            return context
        ##############################

        try:
            sinaptera_configuration, created = SinapteraConfiguration.objects.get_or_create(
                user=self.request.user
            )

        except Exception as e:
            messages.error(
                self.request,
                "An error occurred while trying to fetch the Sinaptera configuration."
            )

            logger.error(
                f"Error while fetching Sinaptera configuration: {e}"
            )

            return context

        context["sinaptera_configuration"] = sinaptera_configuration

        context["cost_multiplier"] = estimate_sinaptera_cost_multiplier(
            N=sinaptera_configuration.branching_factor,
            M=sinaptera_configuration.branch_keeping_factor,
            D=sinaptera_configuration.evaluation_depth_factor
        )

        context["time_multiplier"] = estimate_sinaptera_speed_percentage(
            N=sinaptera_configuration.branching_factor,
            M=sinaptera_configuration.branch_keeping_factor,
            D=sinaptera_configuration.evaluation_depth_factor
        )

        context["accuracy_multiplier"] = estimate_sinaptera_accuracy(
            N=sinaptera_configuration.branching_factor,
            M=sinaptera_configuration.branch_keeping_factor,
            D=sinaptera_configuration.evaluation_depth_factor
        )

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - USE_SINAPTERA_CONFIGURATION
        if not UserPermissionManager.is_authorized(
            user=request.user,
            operation=PermissionNames.USE_SINAPTERA_CONFIGURATION
        ):
            messages.error(
                request,
                "You do not have permission to update Sinaptera configurations."
            )

            logger.error(
                f"User {request.user} does not have permission to update Sinaptera configurations."
            )

            return redirect("sinaptera:configuration")
        ##############################

        try:
            sinaptera_configuration = SinapteraConfiguration.objects.get(
                user=request.user
            )

        except SinapteraConfiguration.DoesNotExist:
            messages.error(
                request,
                "Could not find your Sinaptera configuration. Please try again."
            )

            logger.error(
                f"Could not find Sinaptera configuration for user {request.user}."
            )

            return redirect("sinaptera:configuration")

        # Update boolean fields

        sinaptera_configuration.nitro_boost = request.POST.get(
            "nitro_boost"
        ) == "on"

        sinaptera_configuration.is_active_on_assistants = request.POST.get(
            "is_active_on_assistants"
        ) == "on"

        sinaptera_configuration.is_active_on_leanmods = request.POST.get(
            "is_active_on_leanmods"
        ) == "on"

        sinaptera_configuration.is_active_on_orchestrators = request.POST.get(
            "is_active_on_orchestrators"
        ) == "on"

        sinaptera_configuration.is_active_on_voidforgers = request.POST.get(
            "is_active_on_voidforgers"
        ) == "on"

        # Update integer fields

        int_fields = [
            "rubric_weight_comprehensiveness",
            "rubric_weight_accuracy",
            "rubric_weight_relevancy",
            "rubric_weight_cohesiveness",
            "rubric_weight_diligence",
            "rubric_weight_grammar",
            "rubric_weight_naturalness",

            #####

            "branching_factor",
            "branch_keeping_factor",
            "evaluation_depth_factor"
        ]

        branching_factor = int(request.POST.get("branching_factor", "0"))
        branch_keeping_factor = int(request.POST.get("branch_keeping_factor", "0"))
        evaluation_depth_factor = int(request.POST.get("evaluation_depth_factor", "0"))

        if branch_keeping_factor > branching_factor:
            messages.error(request, "Branch Keeping Factor cannot be greater than Branching Factor.")
            logger.error(f"Branch Keeping Factor cannot be greater than Branching Factor.")

            return redirect("sinaptera:configuration")

        if branch_keeping_factor < 1:
            messages.error(request, "Branch Keeping Factor must be at least 1.")
            logger.error(f"Branch Keeping Factor must be at least 1.")

            return redirect("sinaptera:configuration")

        if branching_factor < 1:
            messages.error(request, "Branching Factor must be at least 1.")
            logger.error(f"Branching Factor must be at least 1.")

            return redirect("sinaptera:configuration")

        if evaluation_depth_factor < 0 or evaluation_depth_factor > 10:
            messages.error(request, "Evaluation Depth Factor must be between 0 and 10.")
            logger.error(f"Evaluation Depth Factor must be between 0 and 10.")

            return redirect("sinaptera:configuration")

        for field_name in int_fields:

            try:
                setattr(sinaptera_configuration, field_name, int(request.POST.get(field_name, "0")))

            except ValueError:
                messages.error(request, f"Invalid value for {field_name}. Must be an integer.")
                logger.error(f"Invalid value for {field_name}: {request.POST.get(field_name, '0')}")

                return redirect("sinaptera:configuration")

        # Update JSON field

        additional_rubric_criteria_json = request.POST.get(
            "additional_rubric_criteria_json",
            ""
        ).strip()

        print("ADD RUBRIC: ", additional_rubric_criteria_json)

        if additional_rubric_criteria_json and additional_rubric_criteria_json != "[]":

            try:
                parsed_criteria = json.loads(
                    additional_rubric_criteria_json
                )

                sinaptera_configuration.additional_rubric_criteria = parsed_criteria

            except json.JSONDecodeError:
                messages.error(request, "Invalid JSON structure for Additional Rubric Criteria.")

                return redirect("sinaptera:configuration")


        else:

            sinaptera_configuration.additional_rubric_criteria = []

        # Save the configuration

        try:
            sinaptera_configuration.save()

            logger.info(f"User {request.user} updated Sinaptera configuration.")
            messages.success(request, "Sinaptera configuration successfully updated!")

        except Exception as e:
            logger.error(f"Error while saving Sinaptera configuration: {e}")
            messages.error(request, f"An error occurred while saving configuration: {e}")

        return redirect("sinaptera:configuration")
