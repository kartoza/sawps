import logging
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from swaps.models import Profile


logger = logging.getLogger(__name__)


class ProfileView(DetailView):
    template_name = 'user/profile.html'
    model = get_user_model()
    slug_field = 'username'

    def post(self, request, *args, **kwargs):
        if 'slug' not in kwargs:
            raise Http404('Missing username')

        profile = self.model.objects.get(
            username=kwargs['slug']
        )
        if profile != self.request.user:
            raise Http404('Mismatch user')

        profile.first_name = self.request.POST.get('first-name', '')
        profile.last_name = self.request.POST.get('last-name', '')
        profile.organization = self.request.POST.get('organization', '')

        if not Profile.objects.filter(user=profile).exists():
            Profile.objects.create(user=profile)

        profile.swaps_profile.picture = self.request.FILES.get('profile-picture', None)
        profile.swaps_profile.save()
        profile.save()

        return HttpResponseRedirect(request.path_info)
