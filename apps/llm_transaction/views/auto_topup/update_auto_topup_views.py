from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView

from apps.llm_transaction.models import AutoBalanceTopUpModel
from apps.organization.models import Organization
from web_project import TemplateLayout


class UpdateAutomatedTopUpPlan(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        top_up_plan = get_object_or_404(AutoBalanceTopUpModel, id=kwargs.get('plan_id'))
        context.update({
            'plan': top_up_plan,
            'organizations': Organization.objects.filter(users__in=[user]),
        })
        return context

    def post(self, request, plan_id):
        top_up_plan = get_object_or_404(AutoBalanceTopUpModel, id=plan_id)
        top_up_plan.on_balance_threshold_trigger = request.POST.get('on_balance_threshold_trigger') == 'on' or False
        top_up_plan.on_interval_by_days_trigger = request.POST.get('on_interval_by_days_trigger') == 'on' or False
        top_up_plan.balance_lower_trigger_threshold_value = request.POST.get(
            'balance_lower_trigger_threshold_value') or 0
        top_up_plan.addition_on_balance_threshold_trigger = request.POST.get(
            'addition_on_balance_threshold_trigger') or 0
        top_up_plan.regular_by_days_interval = request.POST.get('regular_by_days_interval') or 0
        top_up_plan.addition_on_interval_by_days_trigger = request.POST.get(
            'addition_on_interval_by_days_trigger') or 0
        top_up_plan.monthly_hard_limit_auto_addition_amount = request.POST.get(
            'monthly_hard_limit_auto_addition_amount') or 0
        top_up_plan.date_of_last_auto_top_up = timezone.now()  # Update as needed
        top_up_plan.save()
        return redirect('llm_transaction:auto_top_up_list')
