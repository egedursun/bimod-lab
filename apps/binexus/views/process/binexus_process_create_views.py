#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_process_create_views.py
#  Last Modified: 2024-10-22 18:38:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 18:38:43
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
from django.views.generic import TemplateView

from apps.binexus.models import BinexusProcess
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class BinexusView_ProcessCreate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        llm_models = LLMCore.objects.filter(organization__in=user_orgs)
        context['organizations'] = user_orgs
        context['llm_models'] = llm_models
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_BINEXUS_PROCESSES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_BINEXUS_PROCESSES):
            messages.error(self.request, "You do not have permission to create Binexus Processes.")
            return redirect('binexus:process_list')
        ##############################

        organization = request.POST.get('organization')
        llm_model = request.POST.get('llm_model')
        process_name = request.POST.get('process_name')
        process_description = request.POST.get('process_description')
        process_objective = request.POST.get('process_objective')
        process_success_criteria = request.POST.get('process_success_criteria')
        fitness_manager_selectiveness = request.POST.get('fitness_manager_selectiveness')

        gene_names = request.POST.getlist('additional_genes_keys[]')
        gene_values = request.POST.getlist('additional_genes_values[]')

        genes_data = {}
        for i in range(len(gene_names)):
            try:
                gene_name = gene_names[i].strip()
                raw_values = gene_values[i].strip()
                values_list = [v.strip() for v in raw_values.split(',') if v.strip()]
                if gene_name and values_list:
                    genes_data[gene_name] = values_list
            except Exception as e:
                logger.error(f"Error parsing gene data: {e}")
                continue

        optimization_generations = request.POST.get('optimization_generations')
        optimization_population_size = request.POST.get('optimization_population_size')
        optimization_breeding_pool_rate = request.POST.get('optimization_breeding_pool_rate')
        optimization_mutation_rate_per_individual = request.POST.get('optimization_mutation_rate_per_individual')
        optimization_mutation_rate_per_gene = request.POST.get('optimization_mutation_rate_per_gene')
        optimization_crossover_rate = request.POST.get('optimization_crossover_rate')
        self_breeding_possible = request.POST.get('self_breeding_possible') == 'on'

        binexus_process = BinexusProcess.objects.create(
            organization_id=organization,
            llm_model_id=llm_model,
            process_name=process_name,
            process_description=process_description,
            process_objective=process_objective,
            process_success_criteria=process_success_criteria,
            fitness_manager_selectiveness=fitness_manager_selectiveness,
            optimization_generations=optimization_generations,
            optimization_population_size=optimization_population_size,
            optimization_breeding_pool_rate=optimization_breeding_pool_rate,
            optimization_mutation_rate_per_individual=optimization_mutation_rate_per_individual,
            optimization_mutation_rate_per_gene=optimization_mutation_rate_per_gene,
            optimization_crossover_rate=optimization_crossover_rate,
            additional_genes=genes_data,
            self_breeding_possible=self_breeding_possible,
            created_by_user=request.user
        )
        binexus_process.save()

        logger.info(f"Binexus Process created successfully.")
        return redirect('binexus:process_list')
