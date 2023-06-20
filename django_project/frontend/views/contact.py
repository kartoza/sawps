from django.views.generic import TemplateView


class ContactView(TemplateView):
    """
    ContactView displays the contact page by rendering the 'contact.html' template.
    """

    template_name = 'contact.html'
