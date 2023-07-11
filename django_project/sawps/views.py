import logging
from django.shortcuts import redirect, render
from django.contrib.auth import models
from django.contrib.auth import login
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views.generic import View
from stakeholder.models import Organisation, OrganisationInvites, OrganisationUser, UserProfile
from sawps.email_verification_token import email_verification_token


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

class AddUserToOrganisation(View):
    def adduser(self,user,organisation,*args,**kwargs):
        '''when the user has been invited to join an organisation 
        this view will Add the User to the OrganisationUser and update the linked models
        OrganisationInvites, UserProfile'''

        print(user.pk)
        # update organisation invties 
        try:
            
            org = Organisation.objects.get(name=str(organisation))
            org_invites = OrganisationInvites.objects.filter(email=user.email, organisation=org)
            for invite in org_invites:
                if not invite.joined:
                    # Update the joined field to True
                    invite.joined = True
                    invite.save()
                    user_role = invite.user_role
                    # add user to organisation users
                    org_user = OrganisationUser.objects.create(user=user,organisation=org)
                    org_user.save()
                    # add user profile with the role
                    user_profile = UserProfile.objects.create(user=user,user_role_type_id=user_role)
                    user_profile.save()         
        except OrganisationInvites.DoesNotExist:
            org_invites = None
        except Organisation.DoesNotExist:
            org = None

    def is_user_already_joined(self,email,organisation):
        """
        Check if user already joined the organisation
        """

        try:
            org = Organisation.objects.get(name=str(organisation))
            joined = OrganisationInvites.objects.get(email=email, organisation_id=org)
            if joined:
                return True
            else : return False
        except OrganisationInvites.DoesNotExist:
            return None
        except Organisation.DoesNotExist:
            return None
        
        
