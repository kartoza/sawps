from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm
from django import forms
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sawps.email_verification_token import email_verification_token
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings
from sawps.views import AddUserToOrganisation
from django.shortcuts import redirect


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=150, label='First Name', required=True
    )
    last_name = forms.CharField(
        max_length=150, label='Last Name', required=True
    )
    organisation = forms.CharField(
        label='organisation',
        max_length=150, 
        widget=forms.HiddenInput(),
        required=False
    )
   
    field_order = [
        'first_name',
        'last_name',
        'email',
        'password',
        'organisation'
    ]

    def custom_signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False
        user.save()
        # add user to organisation
        if self.cleaned_data.get('organisation'):
            add_user_view = AddUserToOrganisation()
            if add_user_view.is_user_already_joined(self.cleaned_data['email'],self.cleaned_data['organisation']):
                print('adding user')
                add_user_view.adduser(user,self.cleaned_data['organisation'])
            else:
                return redirect('/accounts/login') 


        token = email_verification_token.make_token(user)
        subject = 'Sucess! your SAWPS account has been created'
        message = render_to_string(
            'email/email_verification.html',
            {
                'name': user.first_name,
                'domain': Site.objects.get_current().domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
                'support_email': 'amy@kartoza.com'
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
        self.fields['organisation'].label = 'organisation'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = ''



class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
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
    
    
