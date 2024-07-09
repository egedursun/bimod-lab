import datetime
import decimal

from django.db import models

from apps.llm_transaction.utils import calculate_number_of_tokens, calculate_llm_cost, calculate_internal_service_cost, \
    calculate_tax_cost, calculate_total_cost, calculate_billable_cost

ENCODING_ENGINES = [
    ("cl100k_base", "cl100k_base"),
    ("p50k_base", "p50k_base"),
    ("r50k_base", "r50k_base"),
]


# Create your models here.

class LLMTransaction(models.Model):
    responsible_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='transactions', default=1,
                                         null=True)
    responsible_assistant = models.ForeignKey('assistants.Assistant', on_delete=models.SET_NULL,
                                              related_name='transactions',
                                              null=True, blank=True)
    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL, related_name='transactions',
                                     null=True)
    model = models.ForeignKey('llm_core.LLMCore', on_delete=models.SET_NULL, related_name='transactions',
                              null=True)
    encoding_engine = models.CharField(max_length=100, choices=ENCODING_ENGINES, default="cl100k_base")
    transaction_context_content = models.TextField(default="", blank=True)

    number_of_tokens = models.IntegerField(null=True, blank=True)
    llm_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    internal_service_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    tax_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    total_billable_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.responsible_user.username} - {self.created_at}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.transaction_context_content:
            self.number_of_tokens = calculate_number_of_tokens(self.encoding_engine, self.transaction_context_content)
            # Calculate the costs
            self.llm_cost = calculate_llm_cost(self.model.model_name, self.number_of_tokens)
            self.internal_service_cost = calculate_internal_service_cost(self.llm_cost)
            self.tax_cost = calculate_tax_cost(self.internal_service_cost)
            self.total_billable_cost = calculate_billable_cost(self.internal_service_cost, self.tax_cost)
            self.total_cost = calculate_total_cost(self.llm_cost, self.total_billable_cost)

        # Reduce the transaction billable amount from the organization's balance
        self.organization.balance -= decimal.Decimal().from_float(self.total_billable_cost)
        # Update the transaction's organization
        self.organization.save()
        super().save(*args, **kwargs)
