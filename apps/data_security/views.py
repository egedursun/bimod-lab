from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.data_security.forms import NERIntegrationForm
from apps.data_security.models import NERIntegration
from apps.organization.models import Organization
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
        form = NERIntegrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data_security:list_ner_integrations')

        return render(request, self.template_name, {'form': form})


class ListNERIntegrationsView(TemplateView):
    template_name = 'data_security/ner/list_ner_integrations.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['ner_integrations'] = NERIntegration.objects.select_related('organization').all()
        return context


class UpdateNERIntegrationView(LoginRequiredMixin, TemplateView):
    template_name = 'data_security/ner/update_ner_integration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        ner_integration = NERIntegration.objects.get(id=self.kwargs['pk'])
        context['ner_integration'] = ner_integration
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])

        # Boolean fields for switches
        context['boolean_fields'] = [
            {'name': 'encrypt_persons', 'label': 'Encrypt Persons (PERSON)',
             'value': ner_integration.encrypt_persons},
            {'name': 'encrypt_orgs', 'label': 'Encrypt Organizations (ORG)',
             'value': ner_integration.encrypt_orgs},
            {'name': 'encrypt_nationality_religion_political', 'label': 'Encrypt NORP',
             'value': ner_integration.encrypt_nationality_religion_political},
            {'name': 'encrypt_facilities', 'label': 'Encrypt Facilities (FAC)',
             'value': ner_integration.encrypt_facilities},
            {'name': 'encrypt_countries_cities_states', 'label': 'Encrypt GPE',
             'value': ner_integration.encrypt_countries_cities_states},
            {'name': 'encrypt_locations', 'label': 'Encrypt Locations (LOC)',
             'value': ner_integration.encrypt_locations},
            {'name': 'encrypt_products', 'label': 'Encrypt Products (PRODUCT)',
             'value': ner_integration.encrypt_products},
            {'name': 'encrypt_events', 'label': 'Encrypt Events (EVENT)', 'value': ner_integration.encrypt_events},
            {'name': 'encrypt_artworks', 'label': 'Encrypt Work of Art (WORK_OF_ART)',
             'value': ner_integration.encrypt_artworks},
            {'name': 'encrypt_laws', 'label': 'Encrypt Laws (LAW)', 'value': ner_integration.encrypt_laws},
            {'name': 'encrypt_languages', 'label': 'Encrypt Languages (LANGUAGE)',
             'value': ner_integration.encrypt_languages},
            {'name': 'encrypt_dates', 'label': 'Encrypt Dates (DATE)', 'value': ner_integration.encrypt_dates},
            {'name': 'encrypt_times', 'label': 'Encrypt Times (TIME)', 'value': ner_integration.encrypt_times},
            {'name': 'encrypt_percentages', 'label': 'Encrypt Percentages (PERCENT)',
             'value': ner_integration.encrypt_percentages},
            {'name': 'encrypt_money', 'label': 'Encrypt Money (MONEY)', 'value': ner_integration.encrypt_money},
            {'name': 'encrypt_quantities', 'label': 'Encrypt Quantities (QUANTITY)',
             'value': ner_integration.encrypt_quantities},
            {'name': 'encrypt_ordinal_numbers', 'label': 'Encrypt Ordinal Numbers (ORDINAL)',
             'value': ner_integration.encrypt_ordinal_numbers},
            {'name': 'encrypt_cardinal_numbers', 'label': 'Encrypt Cardinal Numbers (CARDINAL)',
             'value': ner_integration.encrypt_cardinal_numbers},
        ]

        return context

    def post(self, request, *args, **kwargs):
        # Fetch the existing NERIntegration object
        ner_integration = NERIntegration.objects.get(id=self.kwargs['pk'])
        # Manually set each checkbox field based on POST data
        ner_integration.encrypt_persons = request.POST.get('encrypt_persons') == 'True'
        ner_integration.encrypt_orgs = request.POST.get('encrypt_orgs') == 'True'
        ner_integration.encrypt_nationality_religion_political = request.POST.get('encrypt_nationality_religion_political') == 'True'
        ner_integration.encrypt_facilities = request.POST.get('encrypt_facilities') == 'True'
        ner_integration.encrypt_countries_cities_states = request.POST.get('encrypt_countries_cities_states') == 'True'
        ner_integration.encrypt_locations = request.POST.get('encrypt_locations') == 'True'
        ner_integration.encrypt_products = request.POST.get('encrypt_products') == 'True'
        ner_integration.encrypt_events = request.POST.get('encrypt_events') == 'True'
        ner_integration.encrypt_artworks = request.POST.get('encrypt_artworks') == 'True'
        ner_integration.encrypt_laws = request.POST.get('encrypt_laws') == 'True'
        ner_integration.encrypt_languages = request.POST.get('encrypt_languages') == 'True'
        ner_integration.encrypt_dates = request.POST.get('encrypt_dates') == 'True'
        ner_integration.encrypt_times = request.POST.get('encrypt_times') == 'True'
        ner_integration.encrypt_percentages = request.POST.get('encrypt_percentages') == 'True'
        ner_integration.encrypt_money = request.POST.get('encrypt_money') == 'True'
        ner_integration.encrypt_quantities = request.POST.get('encrypt_quantities') == 'True'
        ner_integration.encrypt_ordinal_numbers = request.POST.get('encrypt_ordinal_numbers') == 'True'
        ner_integration.encrypt_cardinal_numbers = request.POST.get('encrypt_cardinal_numbers') == 'True'
        # Update other fields manually
        ner_integration.name = request.POST.get('name')
        ner_integration.description = request.POST.get('description')
        ner_integration.language = request.POST.get('language')
        # Update organization manually (you'll need to fetch the organization)
        organization_id = request.POST.get('organization')
        if organization_id:
            ner_integration.organization_id = organization_id  # Assign organization directly
        # Save the updated NERIntegration object
        ner_integration.save()
        # Redirect to the list page after saving
        return redirect('data_security:update_ner_integration', pk=ner_integration.id)


class DeleteNERIntegrationView(LoginRequiredMixin, TemplateView):
    template_name = 'data_security/ner/confirm_delete_ner_integration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        ner_integration = get_object_or_404(NERIntegration, id=self.kwargs['pk'])
        context['ner_integration'] = ner_integration
        return context

    def post(self, request, *args, **kwargs):
        ner_integration = get_object_or_404(NERIntegration, id=self.kwargs['pk'])
        # If you want, you can add more logic here (e.g., checking permissions)
        ner_integration.delete()
        messages.success(request, 'NER Policy has been deleted successfully.')
        return redirect('data_security:list_ner_integrations')
