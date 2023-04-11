from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    HomeView displays the home page by rendering the 'home.html' template.
    """
    template_name = 'home.html'
