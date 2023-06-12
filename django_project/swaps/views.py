import logging
from django.shortcuts import redirect, render
from django.contrib.auth import models
from django.contrib.auth import login
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views.generic import View
from swaps.email_verification_token import email_verification_token


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        uid = force_str(urlsafe_base64_decode(uidb64))
        try:
            user = models.User.objects.get(pk=uid)
        except models.User.DoesNotExist:
            user = None

        if user is not None and email_verification_token.check_token(
            user, token
        ):
            user.is_active = True
            user.save()
            login(
                request,
                user,
                backend='django.contrib.auth.backends.ModelBackend',
            )
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('/accounts/two-factor/two_factor/setup')
        else:
            messages.warning(
                request,
                (
                    'The confirmation link was invalid, possibly because it has already been used.'
                ),
            )
            return redirect('home')
