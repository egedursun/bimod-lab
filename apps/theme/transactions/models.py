#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: models.py
#  Last Modified: 2024-06-28 20:47:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#

from django.db import models


class Transaction(models.Model):
    customer = models.CharField(max_length=150)
    transaction_date = models.DateField()
    due_date = models.DateField()
    total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Paid", "Paid"), ("Due", "Due"), ("Canceled", "Canceled")])

    def __str__(self):
        return self.customer
