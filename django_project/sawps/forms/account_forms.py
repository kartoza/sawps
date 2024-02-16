from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm
from django import forms
import re
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sawps.email_verification_token import email_verification_token
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings
from sawps.views import AddUserToOrganisation
from django.shortcuts import redirect
from stakeholder.models import OrganisationInvites


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=150, label='First Name', required=True
    )
    last_name = forms.CharField(
        max_length=150, label='Last Name', required=True
    )
    invitation_uuid = forms.CharField(
        label='invitation_uuid',
        max_length=150,
        widget=forms.HiddenInput(),
        required=False
    )

    field_order = [
        'first_name',
        'last_name',
        'email',
        'password',
        'invitation_uuid'
    ]

    def custom_signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False
        user.save()
        # add user to organisation
        if self.cleaned_data.get('invitation_uuid'):
            add_user_view = AddUserToOrganisation()
            is_user_invited = add_user_view.is_user_invited(
                self.cleaned_data['invitation_uuid']
            )
            if is_user_invited:
                add_user_view.adduser(
                    self.cleaned_data['invitation_uuid'])
            else:
                return redirect('/accounts/login')

        token = email_verification_token.make_token(user)
        subject = 'Sucess! your SAWPS account has been created'
        message = render_to_string(
            'emails/email_verification.html',
            {
                'name': user.first_name,
                'domain': Site.objects.get_current().domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
                'support_email': settings.SUPPORT_EMAIL
            },
        )

        send_mail(
            subject,
            None,
            settings.SERVER_EMAIL,
            [user.email],
            html_message=message

        )


        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['invitation_uuid'].label = 'invitation_uuid'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = ''



class CustomLoginForm(LoginForm):

    def get_initial_email(self, kwargs):
        request = kwargs.get('request', None)
        if request is None:
            return None
        next_url = request.GET.get('next', None)
        if next_url is None:
            return None
        email = None
        add_user_re = re.compile(
            '/adduser/([0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15})/?',
            re.I
        )
        results = add_user_re.search(next_url)
        if results:
            invite_uuid = results.group(1)
            org_invite = OrganisationInvites.objects.filter(
                uuid=invite_uuid
            ).order_by('id').last()
            email = org_invite.email if org_invite else None
        return email

    def __init__(self, *args, **kwargs):
        email = self.get_initial_email(kwargs)
        if email:
            kwargs['initial'] = {
                'login': email
            }
        super().__init__(*args, **kwargs)
        self.fields['login'].label = 'Email'
        self.label_suffix = ""


class CustomChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirm New Password'
        self.label_suffix = ""
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = ''
