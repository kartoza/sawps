from stakeholder.models import (
    UserProfile,
    UserRoleType,
    SUPERUSER_ROLE,
    ADMIN_ROLE,
    DATA_CONTRIBUTOR_ROLE
)


class UserProfileMiddleware:
    """Middleware to inject UserProfile to request.
    
    This class must be placed after SessionMiddleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.is_authenticated:
            request.user_profile = UserProfile.objects.filter(
                user=request.user
            ).first()
            if request.user_profile is None:
                # create default profile based on superuser/staff flags
                role = DATA_CONTRIBUTOR_ROLE
                if request.user.is_superuser:
                     role = SUPERUSER_ROLE
                elif request.user.is_staff:
                    role = ADMIN_ROLE
                request.user_profile = UserProfile.objects.create(
                    user=request.user,
                    user_role_type=UserRoleType.objects.filter(
                        name=role
                    ).first()
                )
        response = self.get_response(request)
        return response
