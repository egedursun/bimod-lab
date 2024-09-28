from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.data_security.forms import NERIntegrationForm
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateNERIntegrationView(LoginRequiredMixin, TemplateView):
    template_name = 'data_security/ner/create_ner_integration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = NERIntegrationForm()
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['boolean_fields'] = [
            {'name': 'encrypt_persons', 'label': 'Encrypt Persons (PERSON)'},
            {'name': 'encrypt_orgs', 'label': 'Encrypt Organizations (ORG)'},
            {'name': 'encrypt_nationality_religion_political', 'label': 'Encrypt NORP'},
            {'name': 'encrypt_facilities', 'label': 'Encrypt Facilities (FAC)'},
            {'name': 'encrypt_countries_cities_states', 'label': 'Encrypt GPE'},
            {'name': 'encrypt_locations', 'label': 'Encrypt Locations (LOC)'},
            {'name': 'encrypt_products', 'label': 'Encrypt Products (PRODUCT)'},
            {'name': 'encrypt_events', 'label': 'Encrypt Events (EVENT)'},
            {'name': 'encrypt_artworks', 'label': 'Encrypt Work of Art (WORK_OF_ART)'},
            {'name': 'encrypt_laws', 'label': 'Encrypt Laws (LAW)'},
            {'name': 'encrypt_languages', 'label': 'Encrypt Languages (LANGUAGE)'},
            {'name': 'encrypt_dates', 'label': 'Encrypt Dates (DATE)'},
            {'name': 'encrypt_times', 'label': 'Encrypt Times (TIME)'},
            {'name': 'encrypt_percentages', 'label': 'Encrypt Percentages (PERCENT)'},
            {'name': 'encrypt_money', 'label': 'Encrypt Money (MONEY)'},
            {'name': 'encrypt_quantities', 'label': 'Encrypt Quantities (QUANTITY)'},
            {'name': 'encrypt_ordinal_numbers', 'label': 'Encrypt Ordinal Numbers (ORDINAL)'},
            {'name': 'encrypt_cardinal_numbers', 'label': 'Encrypt Cardinal Numbers (CARDINAL)'},
        ]
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_DATA_SECURITY
        if not UserPermissionManager.is_authorized(user=context_user, operation=PermissionNames.ADD_DATA_SECURITY):
            messages.error(request, "You do not have permission to add data security layers.")
            return redirect('data_security:list_ner_integrations')
        ##############################

        form = NERIntegrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data_security:list_ner_integrations')

        return render(request, self.template_name, {'form': form})
