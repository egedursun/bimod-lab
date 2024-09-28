import uuid
from decimal import Decimal

from django.db import models
from django.utils import timezone

from apps.llm_transaction.utils import INVOICE_TYPES, PAYMENT_METHODS, barcode_generator, invoice_paper_generator


class TransactionInvoice(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='transaction_invoices')
    responsible_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='transaction_invoices',
                                         null=True, blank=True)
    transaction_type = models.CharField(max_length=50, choices=INVOICE_TYPES, default="top-up")
    amount_added = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default="credit-card")
    transaction_date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=2000, null=True, blank=True)
    barcode_image = models.ImageField(upload_to='invoice_barcodes/%Y/%m/%d/', null=True, blank=True)
    transaction_paper = models.FileField(upload_to='transaction_papers/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} @ {self.organization} by {self.responsible_user} on {self.transaction_date}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            # Handle new record creation
            self.transaction_date = timezone.now()
            current_date = self.transaction_date.strftime("%Y%m%d")
            current_year = self.transaction_date.strftime("%Y")
            current_month = self.transaction_date.strftime("%m")
            current_day = self.transaction_date.strftime("%d")
            hashed_date = str(hash(current_date))
            org_id = str(self.organization.id)
            hashed_org_id = str(hash(org_id))
            user_id = str(self.responsible_user.id)
            hashed_user_id = str(hash(user_id))
            random_uuid = str(uuid.uuid4().hex)
            hashed_amount = str(hash(self.amount_added))
            hashed_payment_method = str(hash(self.payment_method))

            # Combine all the hashes
            combined_hash = f"BIMOD-{current_year}{current_month}{current_day}-{org_id}{user_id}{random_uuid}-{hashed_date}{hashed_org_id}{hashed_user_id}{hashed_amount}{hashed_payment_method}".upper()
            self.invoice_number = combined_hash

            # Generate the barcode image
            barcode = barcode_generator(combined_hash)
            if barcode:
                self.barcode_image = barcode

            # Generate the invoice paper
            filename, invoice_paper = invoice_paper_generator(self, barcode)
            if invoice_paper:
                self.transaction_paper.save(filename, invoice_paper, save=False)

            # Call save with update_fields when all fields are initially set
            super().save(force_insert, force_update, using, update_fields)
        else:
            # For existing records, just call the base class save method
            super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "Transaction Invoice"
        verbose_name_plural = "Transaction Invoices"
        ordering = ["-transaction_date"]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['responsible_user']),
            models.Index(fields=['transaction_date']),
            models.Index(fields=['organization', 'transaction_date']),
            models.Index(fields=['organization', 'responsible_user', 'transaction_date']),
        ]
