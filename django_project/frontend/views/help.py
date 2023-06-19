from django.views.generic import TemplateView


class HelpView(TemplateView):
    """
    HelpView displays the help page by rendering the 'help.html' template.
    """

    template_name = 'help.html'
