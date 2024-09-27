from django.views.generic import TemplateView

from web_project import TemplateLayout, TemplateHelper


class IntegrationToOrganizationsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update(
            {
                "layout": "blank", "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
                "display_customizer": False,
            }
        )
        # map_context according to updated context values
        TemplateHelper.map_context(context)
        return context
