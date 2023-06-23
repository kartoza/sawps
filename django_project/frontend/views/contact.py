from .base_view import RegisteredOrganisationBaseView


class ContactView(RegisteredOrganisationBaseView):
    """
    ContactView displays the contact page by rendering the 'contact.html' template.
    """

    template_name = 'contact.html'
