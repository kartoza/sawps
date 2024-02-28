from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import models
from django.contrib.auth import login
from django.contrib import messages
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode
)
from django.utils.encoding import force_str
from django.views.generic import View
from django.contrib.auth.mixins import UserPassesTestMixin
from core.settings.contrib import SUPPORT_EMAIL
from stakeholder.models import (
    OrganisationInvites,
    OrganisationUser,
    OrganisationRepresentative,
    MANAGER,
    UserProfile
)
from sawps.email_verification_token import email_verification_token
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.urls import reverse


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
            messages.success(request, ('Your account have been confirmed.'),
                             extra_tags='notification')
            # find invites that user has joined if any
            org_invite = OrganisationInvites.objects.filter(
                user=user,
                joined=True
            ).order_by('id').last()
            if org_invite:
                AddUserToOrganisation.notify_join_organisation_message(
                    request, org_invite)
            return redirect('/accounts/two-factor/setup')
        else:
            messages.warning(
                request,
                (
                    'The confirmation link was invalid,' +
                    'possibly because it has already been used.'
                ),
                extra_tags='notification'
            )
            return redirect('home')


class AddUserToOrganisation(UserPassesTestMixin, View):

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        # validate if user in invitation is the same with logged in user
        invitation_uuid = self.kwargs.get('invitation_uuid')
        org_invite = OrganisationInvites.objects.filter(
            uuid=invitation_uuid
        ).order_by('id').last()
        if not org_invite:
            return False
        user = org_invite.get_invitee()
        if user is None:
            return False
        return user.id == self.request.user.id

    @staticmethod
    def notify_join_organisation_message(request, org_invite):
        messages.success(
            request,
            (
                'You have successfully joined organisation '
                f'{org_invite.organisation.name} '
                'using the invitation link.'
            ),
            extra_tags='notification'
        )

    def get(self, request, invitation_uuid, *args, **kwargs):
        org_invite = self.adduser(invitation_uuid, *args, **kwargs)
        if org_invite:
            self.notify_join_organisation_message(request, org_invite)
        return redirect(
            reverse('organisations', args=[self.request.user.username]))

    def adduser(self, invitation_uuid, *args, **kwargs):
        '''
        when the user has been invited to join an organisation
        this view will Add the User to the OrganisationUser
        and update the linked models
        OrganisationInvites
        '''
        org_invite = OrganisationInvites.objects.filter(
            uuid=invitation_uuid
        ).order_by('id').last()
        if org_invite is None:
            return None
        # Update the joined field to True
        org_invite.joined = True
        org = org_invite.organisation
        user = org_invite.get_invitee()
        org_invite.user = user
        org_invite.save()

        try:
            user_profile = user.user_profile
        except AttributeError:
            user_profile = UserProfile.objects.create(
                user_id=user.id
            )
        user_profile.current_organisation = org
        user_profile.save()

        # check if not already added to prevent duplicates
        org_user = OrganisationUser.objects.filter(
            user=org_invite.user,
            organisation=org
        ).first()
        if not org_user:
            # add user to organisation users
            OrganisationUser.objects.create(
                user=org_invite.user,
                organisation=org
            )

        if org_invite.assigned_as == MANAGER:
            # check if not already added to prevent duplicates
            org_rep = OrganisationRepresentative.objects.filter(
                user=org_invite.user,
                organisation=org
            ).first()
            if not org_rep:
                # add user to organisation users
                org_rep = OrganisationRepresentative.objects.create(
                    user=org_invite.user,
                    organisation=org
                )
                org_rep.save()
        return org_invite

    def is_user_invited(self, invitation_uuid):
        """
        Check if user invited to the organisation
        """

        try:
            OrganisationInvites.objects.get(
                uuid=invitation_uuid
            )
            return True
        except OrganisationInvites.DoesNotExist:
            return False

    def send_invitation_email(self, email_details):
        subject = 'SAWPS Organisation Invitation'
        try:
            # Send email
            message = render_to_string(
                'emails/invitation_email.html',
                {
                    'return_url': email_details['return_url'],
                    'role': email_details['user']['role'],
                    'organisation': email_details['user']['organisation'],
                    'support_email': email_details['support_email'],
                    'email': SUPPORT_EMAIL,
                    'domain': email_details['domain']
                }
            )
            send_mail(
                subject,
                None,
                settings.SERVER_EMAIL,
                [email_details['recipient_email']],
                html_message=message
            )
            return True
        except Exception:
            return False


class SendRequestEmail(View):
    def send_email(self, request):
        organisation = request.POST.get('organisationName')
        request_message = request.POST.get('message')
        subject = 'Organisation Request'
        if request.user.first_name:
            if request.user.last_name:
                name = request.user.first_name + ' ' + request.user.last_name
            else:
                name = request.user.first_name
        else:
            name = request.user.email
        # Send email
        try:
            message = render_to_string(
                'emails/request_organisation_email.html',
                {
                    'domain': Site.objects.get_current().domain,
                    'email_address': request.user.email,
                    'organisation_name': organisation,
                    'name': name,
                    'request_message': request_message
                },
            )
            send_mail(
                subject,
                None,
                settings.SERVER_EMAIL,
                [SUPPORT_EMAIL],
                html_message=message
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': str(e)})


    def dispatch(self, request, *args, **kwargs):
        if request.POST.get('action') == 'sendrequest':
            return self.send_email(request)
        else:
            return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetView(View):
    template_name = 'password_reset.html'

    def send_reset_email(self, request):
        user_email = request.POST.get('email')

        try:
            user = User.objects.get(email=user_email)
            user_name = user.username
            # Generate the reset token and UID
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            # Compose the reset link URL
            reset_link_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={
                        'uidb64': uidb64, 'token': token})
            )
            subject = 'Password Reset Request'
            message = render_to_string(
                'emails/password_reset.html',
                {
                    'domain': Site.objects.get_current().domain,
                    'name': user_name,
                    'reset_password_link': reset_link_url,
                },
            )
            send_mail(
                subject,
                None,
                settings.SERVER_EMAIL,
                [user_email],
                html_message=message
            )

            return render(
                request,
                'password_reset.html',
                {'show_email_message': True}
            )
        except User.DoesNotExist:
            return render(
                request,
                'password_reset.html',
                {'error_message': 'The email address is not registered.'}
            )

    def dispatch(self, request, *args, **kwargs):
        if request.POST.get('action') == 'sendemail':
            return self.send_reset_email(request)
        elif request.method == 'GET':
            return render(
                request,
                'password_reset.html'
            )
        else:
            return super().dispatch(request, *args, **kwargs)


def custom_password_reset_complete_view(request):
    return render(
        request,
        'forgot_password_reset.html',
        {'show_password_message': True}
    )


def health(request):
    return HttpResponse("OK")
