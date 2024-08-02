from django.urls import path

from .views import CreateLLMCoreView, UpdateLLMCoreView, DeleteLLMCoreView, ListLLMCoreView

app_name = "llm_core"

urlpatterns = [
    path('create/', CreateLLMCoreView.as_view(template_name="llm_core/create_llm_core.html"),
         name="create"),
    path('list/', ListLLMCoreView.as_view(template_name="llm_core/list_llm_cores.html"),
         name="list"),
    path('update/<int:pk>/', UpdateLLMCoreView.as_view(template_name="llm_core/update_llm_core.html"),
         name="update"),
    path('delete/<int:pk>/', DeleteLLMCoreView.as_view(template_name="llm_core/llm_core_confirm_delete.html"),
         name="delete")
]
