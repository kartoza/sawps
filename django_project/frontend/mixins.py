from django.contrib.auth.mixins import AccessMixin


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is at least Admin Role."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if (
            not request.user.is_superuser and
            not request.user_profile.is_admin
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
