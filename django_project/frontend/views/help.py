from .base_view import OrganisationBaseView


class HelpView(OrganisationBaseView):
    """
    HelpView displays the help page by rendering the 'help.html' template.
    """

    template_name = 'help.html'
