from django.views.generic import TemplateView
from django.conf import settings


class MapView(TemplateView):
    """
    MapView displays the map page by rendering the 'map.html' template.
    """
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['maptiler_api_key'] = (
            settings.MAPTILER_API_KEY
        )
        return ctx
