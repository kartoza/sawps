

def get_organisation_short_code(
    province_name: str = None,
    organisation_name: str = None,
    with_digit: bool = True,
    OrganisationModel=None
):
    from frontend.utils.organisation import get_abbreviation
    from stakeholder.models import Organisation

    OrganisationModel = OrganisationModel if OrganisationModel else Organisation
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
        try:
            digit = int(
                OrganisationModel.objects.filter(
                    province__name=province_name,
                    name=organisation_name
                ).latest('short_code').short_code[-4:]
            )
        except OrganisationModel.DoesNotExist:
            digit = 1
        digit = "{:04d}".format(digit + 1)
        return f"{province}{organisation}{digit}"
    else:
        return f"{province}{organisation}"
