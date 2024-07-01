import datetime

from django.db import models

from apps.llm_transaction.utils import calculate_number_of_tokens

ENCODING_ENGINES = [
    ("cl100k_base", "cl100k_base"),
    ("p50k_base", "p50k_base"),
    ("r50k_base", "r50k_base"),
]


# Create your models here.

class LLMTransaction(models.Model):
    responsible_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='transactions', default=1)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='transactions')
    model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE, related_name='transactions')
    encoding_engine = models.CharField(max_length=100, choices=ENCODING_ENGINES, default="cl100k_base")
    transaction_context_content = models.TextField(default="", blank=True)

    number_of_tokens = models.IntegerField(null=True, blank=True)
    llm_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    internal_service_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_billable_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization.name} - {self.model.nickname} - {self.created_at}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]
