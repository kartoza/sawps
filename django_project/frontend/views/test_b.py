from django.views.generic import TemplateView


class TestBView(TemplateView):
    """
    HomeView displays the home page by rendering the 'home.html' template.
    """

    template_name = 'test_b.html'
