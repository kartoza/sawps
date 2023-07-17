from allauth_2fa.middleware import BaseRequire2FAMiddleware
from django.conf import settings


class RequireSuperuser2FAMiddleware(BaseRequire2FAMiddleware):
    def require_2fa(self, request):
        # Superusers are require to have 2FA.
        if not settings.DISABLE_2FA:
            return request.user.is_active
        return None
