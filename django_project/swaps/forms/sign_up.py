from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from swaps.email_verification_token import email_verification_token
from django.contrib.sites.models import Site


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=150, label='First Name', required=True
    )
    last_name = forms.CharField(
        max_length=150, label='Last Name', required=True
    )
   
    field_order = [
        'first_name',
        'last_name',
        'email',
        'password',
    ]

    def custom_signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.organisation = self.cleaned_data['organisation']
        try:
            user.groups.set(Group.objects.get(id=self.cleaned_data['group']))
        except Exception:
            pass

        user.is_active = False
        user.save()

        token = email_verification_token.make_token(user)
        subject = 'Verify you e-mail adresse on SWAPS'
        message = render_to_string(
            'email/email_verification.html',
            {
                'email': user.email,
                'domain': Site.objects.get_current().domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            },
        )

        user.email_user(subject, message)
        messages.success(
            request,
            ('Please verify your email addresse to complete registration.'),
        )

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
