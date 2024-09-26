import base64

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.orchestration.orchestration_executor import OrchestrationExecutor
from apps._services.storages.storage_executor import StorageExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.llm_core.models import LLMCore
from apps.orchestrations.forms import MaestroForm
from apps.orchestrations.models import Maestro, OrchestrationQuery, OrchestrationQueryLog, \
    OrchestrationQueryLogTypesNames
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class CreateOrchestrationView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of a new orchestration within the Bimod platform.
    """
    template_name = 'orchestrations/create_orchestration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = MaestroForm()
        context['organizations'] = Organization.objects.filter(users=self.request.user)
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        context['assistants'] = Assistant.objects.filter(organization__in=context['organizations'])
        return context

    def post(self, request, *args, **kwargs):
        form = MaestroForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ORCHESTRATIONS):
            messages.error(self.request, "You do not have permission to create orchestrations.")
            return redirect('orchestrations:list')
        ##############################

        if form.is_valid():
            maestro = form.save(commit=False)
            maestro.created_by_user = request.user
            maestro.last_updated_by_user = request.user
            maestro.save()

            # Save workers
            workers = request.POST.getlist('workers')
            maestro.workers.set(workers)

            return redirect('orchestrations:list')
        else:
            error_messages = form.errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = error_messages
            return self.render_to_response(context)


class OrchestrationListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of orchestrations within the Bimod.io platform.

    This view displays a list of orchestrations that the user has access to. It organizes the orchestrations
    by organization.
    """
    template_name = 'orchestrations/list_orchestrations.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ORCHESTRATIONS):
            messages.error(self.request, "You do not have permission to list orchestrations.")
            return context
        ##############################

        user_organizations = Organization.objects.filter(users__in=[self.request.user])
        orchestrations = Maestro.objects.filter(organization__in=user_organizations)

        # Organizing orchestrations by organization
        orchestrations_by_org = {}
        for org in user_organizations:
            orchestrations_by_org[org] = orchestrations.filter(organization=org)

        context['orchestrations_by_organization'] = orchestrations_by_org
        return context


class OrchestrationUpdateView(LoginRequiredMixin, TemplateView):
    """
    Handles the update of an existing orchestration within the Bimod.io platform.

    This view displays a form for updating an orchestration. Upon form submission, it validates the input and saves the updated orchestration to the database.
    """

    template_name = 'orchestrations/update_orchestration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        orchestration = get_object_or_404(Maestro, pk=kwargs['pk'])
        context['form'] = MaestroForm(instance=orchestration)
        context['orchestration'] = orchestration
        context['organizations'] = Organization.objects.filter(users=self.request.user)
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        context['assistants'] = Assistant.objects.filter(organization__in=context['organizations'])
        context['selected_workers'] = orchestration.workers.all().values_list('id', flat=True)
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_ORCHESTRATIONS):
            messages.error(self.request, "You do not have permission to update orchestrations.")
            return redirect('orchestrations:list')
        ##############################

        orchestration = get_object_or_404(Maestro, pk=kwargs['pk'])
        form = MaestroForm(request.POST, request.FILES, instance=orchestration)

        if form.is_valid():
            updated_orchestration = form.save(commit=False)
            updated_orchestration.last_updated_by_user = request.user  # Update last_updated_by_user field
            updated_orchestration.save()

            # Update workers
            workers = request.POST.getlist('workers')
            updated_orchestration.workers.set(workers)
            return redirect('orchestrations:update', pk=kwargs['pk'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = form.errors
            return self.render_to_response(context)


class OrchestrationDeleteView(LoginRequiredMixin, TemplateView):
    """
    Displays a confirmation page for deleting an orchestration.

    This view displays a confirmation page for deleting an orchestration. It prompts the user to confirm the
    deletion of the orchestration. Upon confirmation, the orchestration is deleted from the database.
    """
    template_name = 'orchestrations/delete_orchestration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        orchestration = get_object_or_404(Maestro, pk=kwargs['pk'])
        context['orchestration'] = orchestration
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ORCHESTRATIONS):
            messages.error(self.request, "You do not have permission to delete orchestrations.")
            return redirect('orchestrations:list')
        ##############################

        orchestration = get_object_or_404(Maestro, pk=kwargs['pk'])
        orchestration_name = orchestration.name
        orchestration.delete()
        messages.success(request, f'Orchestration "{orchestration_name}" has been successfully deleted.')
        return redirect('orchestrations:list')


##############################################################################################################


class OrchestrationQueryListView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        maestro_id = kwargs['pk']
        maestro = get_object_or_404(Maestro, id=maestro_id)
        query_chats = OrchestrationQuery.objects.filter(
            created_by_user=self.request.user, maestro=maestro
        )
        context['maestro'] = maestro
        context['query_chats'] = query_chats
        context['maestro_list'] = Maestro.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # INFO: This is the dedicated method to create a new query for the orchestration.

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_AND_USE_ORCHESTRATION_CHATS):
            messages.error(self.request, "You do not have permission to create and use orchestration queries.")
            return redirect('orchestrations:list')
        ##############################

        maestro_id = request.POST.get('maestro_id')
        query_text = request.POST.get('query_text')

        # 2. Content, image, file, and other inputs retrieval
        attached_images = request.FILES.getlist('attached_images[]')
        attached_files = request.FILES.getlist('attached_files[]')
        print(f"[OrchestrationQueryListView.post] The message content has been extracted successfully.")

        sketch_image = {'sketch_image': None}
        attached_canvas_image = request.POST.get('sketch_image')
        sketch_image_full_uris_list = []
        try:
            sketch_image_bytes = base64.b64decode(attached_canvas_image.split("base64,")[1].encode())
            sketch_image['sketch_image'] = sketch_image_bytes
            sketch_image_full_uris_list = StorageExecutor.save_sketch_images(sketch_image_dict=sketch_image)
        except Exception as e:
            # No image attached
            print(f"[OrchestrationQueryListView.post] Error reading sketch image file: {e}")
            pass
        print(f"[OrchestrationQueryListView.post] The sketch image(s) has been extracted successfully.")

        edit_image_bytes_dict = {'edit_image': None, 'edit_image_mask': None}
        attached_edit_image = request.FILES.get('edit_image')
        attached_edit_image_mask = request.POST.get('edit_image_mask')
        edit_image_full_uris_list = []
        try:
            edit_image_bytes = attached_edit_image.read()
            edit_image_mask_bytes = base64.b64decode(attached_edit_image_mask.split("base64,")[1].encode())
            edit_image_bytes_dict['edit_image'] = edit_image_bytes
            edit_image_bytes_dict['edit_image_mask'] = edit_image_mask_bytes
            edit_image_full_uris_list = StorageExecutor.save_edit_images(edit_image_dict=edit_image_bytes_dict)
        except Exception as e:
            # No image attached
            print(f"[OrchestrationQueryListView.post] Error reading edit image file: {e}")
            pass
        print(f"[OrchestrationQueryListView.post] The edit image(s) has been extracted successfully.")

        # 3. Handle the file and image uploads
        image_bytes_list = []
        for image in attached_images:
            try:
                image_bytes = image.read()
            except Exception as e:
                print(f"[ChatView.post] Error reading image file: {e}")
                continue
            image_bytes_list.append(image_bytes)
        image_full_uris = StorageExecutor.save_images_and_provide_full_uris(image_bytes_list)
        if sketch_image_full_uris_list:
            image_full_uris.extend(sketch_image_full_uris_list)
        if edit_image_full_uris_list:
            image_full_uris.extend(edit_image_full_uris_list)
        print(f"[OrchestrationQueryListView.post] The image(s) has been uploaded successfully.")

        file_bytes_list = []
        for file in attached_files:
            file_name = file.name
            try:
                file_bytes = file.read()
            except Exception as e:
                print(f"[OrchestrationQueryListView.post] Error reading file: {e}")
                continue
            file_bytes_list.append((file_bytes, file_name))
        file_full_uris = StorageExecutor.save_files_and_provide_full_uris(file_bytes_list)
        print(f"[OrchestrationQueryListView.post] The file(s) has been uploaded successfully.")

        record_audio = request.POST.get('record_audio')
        audio_full_uri = None
        if record_audio:
            audio_base_64 = request.POST.get('record_audio')
            audio_bytes = base64.b64decode(audio_base_64.split("base64,")[1].encode())
            audio_full_uri = StorageExecutor.save_files_and_provide_full_uris([(audio_bytes, 'audio.webm')])[0]
            print(f"[OrchestrationQueryListView.post] The audio file has been uploaded successfully.")
        if audio_full_uri:
            file_full_uris.append(audio_full_uri)
            print(f"[OrchestrationQueryListView.post] The audio file has been added to the file URIs list: {file_full_uris}")

        #############################################################################################################

        # Create the query chat and the log for the user query
        maestro = get_object_or_404(Maestro, id=maestro_id)
        query_chat = OrchestrationQuery.objects.create(
            maestro=maestro,
            query_text=query_text,
            created_by_user=request.user,
            last_updated_by_user=request.user
        )

        query_log = OrchestrationQueryLog.objects.create(
            orchestration_query=query_chat,
            log_type=OrchestrationQueryLogTypesNames.USER,
            log_text_content=query_text,
            log_file_contents=None,
            log_image_contents=None,
        )
        query_chat.logs.add(query_log)
        query_chat.save()

        orchestration_executor = OrchestrationExecutor(
            maestro=maestro,
            query_chat=query_chat
        )
        final_response = orchestration_executor.execute_for_query()
        print("[OrchestrationQueryListView.post] Final response retrieved: ", final_response)

        # Redirect to the newly created query's detail page
        return redirect('orchestrations:query_detail', pk=maestro_id, query_id=query_chat.id)


class OrchestrationQueryDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'orchestrations/query_confirm_delete_orchestration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        query_id = self.kwargs['query_id']
        context['query'] = get_object_or_404(OrchestrationQuery, pk=query_id)
        context['orchestration'] = context['query'].maestro
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - REMOVE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_ORCHESTRATION_CHATS):
            messages.error(self.request, "You do not have permission to remove orchestration queries.")
            return redirect('orchestrations:list')
        ##############################

        query_id = self.kwargs['query_id']
        query = get_object_or_404(OrchestrationQuery, pk=query_id)
        maestro_id = query.maestro.id
        query.delete()
        return redirect('orchestrations:query_list', pk=maestro_id)


class OrchestrationQueryDetailView(LoginRequiredMixin, TemplateView):
    template_name = "orchestrations/query_detail_orchestration.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_AND_USE_ORCHESTRATION_CHATS):
            messages.error(self.request, "You do not have permission to create and use orchestration queries.")
            return context
        ##############################

        query_id = self.kwargs.get('query_id')
        query = get_object_or_404(OrchestrationQuery, id=query_id)
        context['query'] = query
        context['logs'] = query.logs.all()
        return context


class OrchestrationQueryRerunView(LoginRequiredMixin, TemplateView):
    template_name = "orchestrations/query_detail_orchestration.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):

        #############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_AND_USE_ORCHESTRATION_CHATS):
            messages.error(self.request, "You do not have permission to create and use orchestration queries.")
            return redirect('orchestrations:list')
        ##############################

        query_id = self.kwargs.get('query_id')
        query = get_object_or_404(OrchestrationQuery, id=query_id)

        query_text = query.query_text

        # delete all previous logs
        query.logs.all().delete()

        # add a new log for the user query
        query_log = OrchestrationQueryLog.objects.create(
            orchestration_query=query,
            log_type=OrchestrationQueryLogTypesNames.USER,
            log_text_content=query_text,
            log_file_contents=None,
            log_image_contents=None,
        )
        query.logs.add(query_log)
        query.save()

        # re-run the query
        orchestration_executor = OrchestrationExecutor(
            maestro=query.maestro,
            query_chat=query
        )
        final_response = orchestration_executor.execute_for_query()
        print("[OrchestrationQueryRerunView.get_context_data] Final response retrieved: ", final_response)

        return redirect('orchestrations:query_detail', pk=query.maestro.id, query_id=query.id)
