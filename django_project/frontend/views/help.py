from .base_view import RegisteredOrganisationBaseView


class HelpView(RegisteredOrganisationBaseView):
    """
    HelpView displays the help page by rendering the 'help.html' template.
    """

    template_name = 'help.html'
