#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: blockchain_contract_admin.py
#  Last Modified: 2024-10-19 22:29:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:29:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


"""
#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: blockchain_contract_models.py
#  Last Modified: 2024-10-19 22:29:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:29:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import os
from django.db import models
from apps.smart_contracts.utils import (SMART_CONTRACT_CATEGORIES, SMART_CONTRACT_TEMPLATE_CHOICES,
                                        SmartContractTemplateNames)
from config.settings import BASE_DIR
import logging

logger = logging.getLogger(__name__)


class BlockchainSmartContract(models.Model):
    wallet = models.ForeignKey('smart_contracts.BlockchainWalletConnection', on_delete=models.CASCADE,
                               related_name='smart_contracts')
    category = models.CharField(max_length=100, choices=SMART_CONTRACT_CATEGORIES)
    contract_template = models.CharField(max_length=100, choices=SMART_CONTRACT_TEMPLATE_CHOICES)
    contract_template_filepath = models.CharField(max_length=1000, null=True, blank=True)

    creation_prompt = models.TextField(blank=True, null=True)
    refinement_iterations_before_evaluation = models.IntegerField(default=3)
    generated_solidity_code = models.TextField(null=True, blank=True)

    deployed = models.BooleanField(default=False)
    deployed_at = models.DateTimeField(null=True, blank=True)
    contract_address = models.CharField(max_length=1000, null=True, blank=True)

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        related_name='smart_contracts_created_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.wallet.organization.name + " - " + self.wallet.nickname + " - " + self.category + ' - ' +
                self.contract_template + ' - ' + self.contract_address)

    class Meta:
        verbose_name = 'Blockchain Smart Contract'
        verbose_name_plural = 'Blockchain Smart Contracts'
        indexes = [
            models.Index(fields=['wallet', 'category', 'contract_template']),
            models.Index(fields=['contract_address']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def save(self, *args, **kwargs):
        if self.contract_template_filepath is None:
            if self.contract_template not in SmartContractTemplateNames.Custom.as_list():
                file_path = os.path.join(BASE_DIR, "apps", "smart_contracts", "templates", "smart_contracts",
                                         self.category, str(self.contract_template + ".sol"))
                self.contract_template_filepath = file_path
            else:
                logger.info("Custom contract template detected. No file path provided.")
                pass
        super(BlockchainSmartContract, self).save(*args, **kwargs)

"""


from django.contrib import admin

from apps.smart_contracts.models import BlockchainSmartContract
from apps.smart_contracts.utils import BLOCKCHAIN_SMART_CONTRACT_ADMIN_LIST, BLOCKCHAIN_SMART_CONTRACT_ADMIN_FILTER, \
    BLOCKCHAIN_SMART_CONTRACT_ADMIN_SEARCH


@admin.register(BlockchainSmartContract)
class BlockchainSmartContractAdmin(admin.ModelAdmin):
    list_display = BLOCKCHAIN_SMART_CONTRACT_ADMIN_LIST
    list_filter = BLOCKCHAIN_SMART_CONTRACT_ADMIN_FILTER
    search_fields = BLOCKCHAIN_SMART_CONTRACT_ADMIN_SEARCH
    ordering = ['created_at', 'updated_at']
