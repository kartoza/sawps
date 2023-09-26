from .base_view import OrganisationBaseView


class HomeView(OrganisationBaseView):
    """
    HomeView displays the home page by rendering the 'home.html' template.
    """

    template_name = 'home.html'
