from celery import shared_task

from apps.llm_transaction.models import OrganizationBalanceSnapshot
from apps.organization.models import Organization


@shared_task
def track_organization_balances():
    all_organizations = Organization.objects.all()
    for organization in all_organizations:
        balance_snapshot = OrganizationBalanceSnapshot(organization=organization, balance=organization.balance)
        balance_snapshot.save()
    return True
