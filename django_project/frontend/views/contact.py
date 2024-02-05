from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .base_view import OrganisationBaseView
from frontend.forms import ContactUsForm


class ContactUsView(OrganisationBaseView, FormView):
    """
    ContactView
    """
    template_name = 'contact.html'
    form_class = ContactUsForm
    success_url = "/"

    def get_initial(self):
        initial = super(ContactUsView, self).get_initial()
        if not self.request.user.is_anonymous:
            initial['name'] = self.request.user.get_full_name()
            initial['email'] = self.request.user.email

        return initial

    def form_valid(self, form):
        form_data = form.cleaned_data

        if not self.request.user.is_anonymous:
            form_data['username'] = self.request.user.username

        subject = form_data['subject']

        # POST to the support email
        recipients = settings.CONTACT_US_RECIPIENTS

        sender = form_data.get('email')
        cc = []
        if form_data['copy']:
            cc.append(sender)

        message = render_to_string(
            'emails/email_contact_us.html',
            {
                'name': form_data['name'],
                'message': form_data['message'],
                'email': form_data['email'],
            },
        )

        email = EmailMultiAlternatives(
            subject,
            message,
            settings.SERVER_EMAIL,
            recipients,
            cc=cc
        )
        email.content_subtype = "html"
        email.send()

        return super(ContactUsView, self).form_valid(form)
