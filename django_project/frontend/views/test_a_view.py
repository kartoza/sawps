from django.views.generic import TemplateView


class TestAView(TemplateView):
    """
    HomeView displays the home page by rendering the 'home.html' template.
    """

    template_name = 'test_a.html'
