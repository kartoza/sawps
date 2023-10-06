from .base_view import OrganisationBaseView


class AboutView(OrganisationBaseView):
    """
    AboutView displays the about page by rendering the 'about.html' template.
    """

    template_name = 'about.html'
