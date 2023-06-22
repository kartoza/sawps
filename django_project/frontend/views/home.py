from .base_view import RegisteredOrganisationBaseView


class HomeView(RegisteredOrganisationBaseView):
    """
    HomeView displays the home page by rendering the 'home.html' template.
    """

    template_name = 'home.html'
