from allauth_2fa.middleware import BaseRequire2FAMiddleware
from django.conf import settings


class RequireSuperuser2FAMiddleware(BaseRequire2FAMiddleware):
    allowed_pages = [
        # They should still be able to log out or change password.
        "account_change_password",
        "account_logout",
        "account_reset_password",
        # URLs required to set up two-factor
        "two-factor-setup",
        "account_resend_verification"
    ]

    def require_2fa(self, request):
        # Superusers are require to have 2FA.
        if not settings.DISABLE_2FA:
            return request.user.is_active
        return None
