from audioop import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.organization.models import Organization
from apps.subscription.forms import SubscriptionForm
from apps.subscription.models import SUBSCRIPTION_PLANS, SUBSCRIPTION_COSTS, SUBSCRIPTION_LIMITS, Subscription
from web_project import TemplateLayout


# Create your views here.

class CreateSubscriptionView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        organizations = Organization.objects.filter(user=user)

        subscription_prices = {}
        for plan, price in SUBSCRIPTION_COSTS.items():
            subscription_prices[plan] = {
                'monthly': price,
                'annual': price * 12 * 0.9
            }
        context.update({
            'organizations': organizations,
            'form': SubscriptionForm(),
            'subscription_plans': SUBSCRIPTION_PLANS,
            'subscription_prices': subscription_prices,
        })

        return context

    def post(self, request, *args, **kwargs):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # retrieve the card number and remove the white spaces
            card_number = form.cleaned_data['card_number']
            card_number = card_number.replace(' ', '')
            form.cleaned_data['card_number'] = card_number
            subscription = form.save(commit=False)
            # retrieve the subscription plan and set the subscription limits accordingly
            subscription_plan = subscription.subscription_plan
            subscription.subscription_cost = SUBSCRIPTION_COSTS[subscription_plan]
            subscription.subscription_balance_discount_rate = 0.0
            subscription.max_number_of_llm_cores = SUBSCRIPTION_LIMITS[subscription_plan]["max_number_of_llm_cores"]
            subscription.max_number_of_users = SUBSCRIPTION_LIMITS[subscription_plan]["max_number_of_users"]
            subscription.max_number_of_assistants = SUBSCRIPTION_LIMITS[subscription_plan]["max_number_of_assistants"]
            subscription.max_number_of_chats = SUBSCRIPTION_LIMITS[subscription_plan]["max_number_of_chats"]
            subscription.max_orchestrations = SUBSCRIPTION_LIMITS[subscription_plan]["orchestrations"]
            subscription.max_providers = SUBSCRIPTION_LIMITS[subscription_plan]["providers"]
            subscription.max_file_systems = SUBSCRIPTION_LIMITS[subscription_plan]["file_systems"]
            subscription.max_web_browsers = SUBSCRIPTION_LIMITS[subscription_plan]["web_browsers"]
            subscription.max_sql_databases = SUBSCRIPTION_LIMITS[subscription_plan]["sql_databases"]
            subscription.max_knowledge_bases = SUBSCRIPTION_LIMITS[subscription_plan]["knowledge_bases"]
            subscription.max_documents = SUBSCRIPTION_LIMITS[subscription_plan]["documents"]
            subscription.max_functions = SUBSCRIPTION_LIMITS[subscription_plan]["functions"]
            subscription.max_api = SUBSCRIPTION_LIMITS[subscription_plan]["api"]
            subscription.max_scheduled_jobs = SUBSCRIPTION_LIMITS[subscription_plan]["scheduled_jobs"]
            subscription.max_triggers = SUBSCRIPTION_LIMITS[subscription_plan]["triggers"]
            subscription.max_integrations = SUBSCRIPTION_LIMITS[subscription_plan]["integrations"]
            subscription.max_meta_integrations = SUBSCRIPTION_LIMITS[subscription_plan]["meta_integrations"]
            subscription.allow_audio_gen_and_analysis = SUBSCRIPTION_LIMITS[subscription_plan]["audio_gen_and_analysis"]
            subscription.allow_image_gen_and_analysis = SUBSCRIPTION_LIMITS[subscription_plan]["image_gen_and_analysis"]
            subscription.allow_long_term_memory = SUBSCRIPTION_LIMITS[subscription_plan]["long_term_memory"]
            subscription.allow_image_storage = SUBSCRIPTION_LIMITS[subscription_plan]["image_storage"]
            subscription.allow_video_storage = SUBSCRIPTION_LIMITS[subscription_plan]["video_storage"]
            subscription.allow_audio_storage = SUBSCRIPTION_LIMITS[subscription_plan]["audio_storage"]
            subscription.user = request.user
            subscription.subscription_status = 'active'
            subscription.save()
            return redirect('subscription:list')
        else:
            context = self.get_context_data(**kwargs)
            error_messages = form.errors
            context['error_messages'] = error_messages
            context['form'] = form
            return self.render_to_response(context)


class ListSubscriptionView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        subscriptions = Subscription.objects.filter(user=user)
        context['subscriptions'] = subscriptions
        return context


class DeleteSubscriptionView(LoginRequiredMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        subscription = get_object_or_404(Subscription, id=kwargs['pk'])
        subscription.delete()
        return redirect('subscription:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(TemplateLayout.init(self, super().get_context_data(**kwargs)))
        return context

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user)
