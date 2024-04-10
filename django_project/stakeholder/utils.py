from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from core.settings.contrib import SUPPORT_EMAIL
from frontend.static_mapping import (
    ORGANISATION_MANAGER,
    ORGANISATION_MEMBER
)
from property.tasks import update_organisation_property_short_code


def get_organisation_short_code(
    province_name: str = None,
    organisation_name: str = None,
    with_digit: bool = True,
    OrganisationModel=None
):
    from frontend.utils.organisation import get_abbreviation
    from stakeholder.models import Organisation

    OrganisationModel = (
        OrganisationModel if OrganisationModel else Organisation
    )
    province_name = province_name if province_name else ''
    organisation_name = organisation_name if organisation_name else ''

    province = get_abbreviation(
        province_name
    ) if province_name else ''
    organisation = get_abbreviation(
        organisation_name
    ) if organisation_name else ''

    if with_digit:
        # instead of using DB count, take next digit based on
        # the latest digit
        obj_latest_code = OrganisationModel.objects.filter(
            province__name=province_name
        ).order_by('short_code').last()

        digit = 1
        if obj_latest_code:
            digit = int(obj_latest_code.short_code[-4:]) + 1
        digit = "{:04d}".format(digit)
        return f"{province}{organisation}{digit}"
    else:
        return f"{province}{organisation}"


def forward_func_0015(Province, Organisation):
    for province in Province.objects.all():
        update_organisation_property_short_code(
            province_id=province.id,
            update_organisation=True,
            update_property=False,
            ProvinceModel=Province,
            OrganisationModel=Organisation
        )

    for org in Organisation.objects.filter(province__isnull=True):
        short_code = get_organisation_short_code(
            province_name='',
            organisation_name=org.name,
            with_digit=True,
            OrganisationModel=Organisation
        )
        org.short_code = short_code
        org.save()


def add_user_to_org_member(
    instance,
    OrgInvModel=None,
    GroupModel=None,
):
    """
    Add user to Organisation Member group.
    """
    from stakeholder.models import OrganisationInvites
    from django.contrib.auth.models import Group

    OrgInvModel = OrgInvModel if OrgInvModel else OrganisationInvites
    GroupModel = GroupModel if GroupModel else Group
    group, _ = GroupModel.objects.get_or_create(name=ORGANISATION_MEMBER)
    instance.user.groups.add(group)


def remove_user_from_org_member(instance):
    """
    Remove user from Organisation Member group.
    """

    from stakeholder.models import OrganisationUser
    from django.contrib.auth.models import Group

    organisation_users = OrganisationUser.objects.filter(user=instance.user)

    # Remove from Data Contributor groups if user is
    # no longer assigned to any organisation
    group = Group.objects.filter(name='Data contributor').first()
    if group:
        instance.user.groups.remove(group)

    if not organisation_users.exists():
        group = Group.objects.filter(name=ORGANISATION_MEMBER).first()
        if group:
            instance.user.groups.remove(group)


def add_user_to_org_manager(
    instance,
    GroupModel=None,
):
    """
    Add user to Organisation Manager group.
    """
    from django.contrib.auth.models import Group

    GroupModel = GroupModel if GroupModel else Group
    group, _ = GroupModel.objects.get_or_create(name=ORGANISATION_MANAGER)
    instance.user.groups.add(group)


def remove_user_from_org_manager(instance):
    """
    Remove user from Organisation Manager group.
    """

    from stakeholder.models import OrganisationRepresentative
    from django.contrib.auth.models import Group

    organisation_reps = OrganisationRepresentative.objects.filter(
        user=instance.user
    )

    if not organisation_reps.exists():
        group = Group.objects.filter(name=ORGANISATION_MANAGER).first()
        if group:
            instance.user.groups.remove(group)


def notify_user_becomes_manager(instance):
    if not instance.user.email:
        return
    # Send email
    subject = 'SAWPS Organisation - You have been made as a manager'
    message = render_to_string(
        'emails/manager_email.html',
        {
            'full_name': instance.user.get_full_name(),
            'organisation': instance.organisation.name,
            'support_email': SUPPORT_EMAIL
        }
    )
    send_mail(
        subject,
        None,
        settings.SERVER_EMAIL,
        [instance.user.email],
        html_message=message
    )
