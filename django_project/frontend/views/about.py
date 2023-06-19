from django.views.generic import TemplateView


class AboutView(TemplateView):
    """
    AboutView displays the about page by rendering the 'about.html' template.
    """

    template_name = 'about.html'
