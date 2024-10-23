#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_process_update_views.py
#  Last Modified: 2024-10-22 18:39:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 18:39:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.binexus.models import BinexusProcess
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class BinexusView_ProcessUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        process_id = self.kwargs.get('pk')
        binexus_process = BinexusProcess.objects.get(id=process_id)
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        llm_models = LLMCore.objects.filter(organization__in=user_orgs)
        context['organizations'] = user_orgs
        context['llm_models'] = llm_models
        context['binexus_process'] = binexus_process
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_BINEXUS_PROCESSES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_BINEXUS_PROCESSES):
            messages.error(self.request, "You do not have permission to update Binexus Processes.")
            return redirect('binexus:process_list')
        ##############################

        process_id = self.kwargs.get('pk')
        binexus_process = BinexusProcess.objects.get(id=process_id)
        binexus_process.organization_id = request.POST.get('organization')
        binexus_process.llm_model_id = request.POST.get('llm_model')
        binexus_process.process_name = request.POST.get('process_name')
        binexus_process.process_description = request.POST.get('process_description')
        binexus_process.process_objective = request.POST.get('process_objective')
        binexus_process.process_success_criteria = request.POST.get('process_success_criteria')
        binexus_process.fitness_manager_selectiveness = request.POST.get('fitness_manager_selectiveness')
        # Optimization Hyper-Parameters
        binexus_process.optimization_generations = request.POST.get('optimization_generations')
        binexus_process.optimization_population_size = request.POST.get('optimization_population_size')
        binexus_process.optimization_breeding_pool_rate = request.POST.get('optimization_breeding_pool_rate')
        binexus_process.optimization_mutation_rate_per_individual = request.POST.get(
            'optimization_mutation_rate_per_individual')
        binexus_process.optimization_mutation_rate_per_gene = request.POST.get('optimization_mutation_rate_per_gene')
        binexus_process.optimization_crossover_rate = request.POST.get('optimization_crossover_rate')
        binexus_process.self_breeding_possible = request.POST.get('self_breeding_possible') == 'on'
        binexus_process.save()
        return redirect('binexus:process_list')
