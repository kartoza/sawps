from .base_view import RegisteredOrganisationBaseView


class AboutView(RegisteredOrganisationBaseView):
    """
    AboutView displays the about page by rendering the 'about.html' template.
    """

    template_name = 'about.html'
