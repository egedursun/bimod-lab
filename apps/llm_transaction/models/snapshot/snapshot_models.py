from django.db import models


class OrganizationBalanceSnapshot(models.Model):
    """
    OrganizationBalanceSnapshot:
    - Purpose: Represents a snapshot of an organization's balance at a specific point in time, used for tracking financial activity and historical records.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` associated with the balance snapshot.
        - `balance`: The balance of the organization at the time of the snapshot.
        - `created_at`: Timestamp for when the snapshot was created.
    - Meta:
        - `verbose_name`: "Organization Balance Snapshot"
        - `verbose_name_plural`: "Organization Balance Snapshots"
        - `ordering`: Orders balance snapshots by creation date in descending order.
        - `indexes`: Indexes on various fields for optimized queries.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL,
                                     related_name='balance_snapshots', null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization} - {self.balance} - {self.created_at}"

    class Meta:
        verbose_name = "Organization Balance Snapshot"
        verbose_name_plural = "Organization Balance Snapshots"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['created_at']),
            models.Index(fields=['organization', 'created_at']),
        ]
