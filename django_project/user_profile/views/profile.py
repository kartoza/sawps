import logging
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from user_profile.models import Profile


logger = logging.getLogger(__name__)


class ProfileView(DetailView):
    template_name = 'user/profile.html'
    model = get_user_model()
    slug_field = 'username'

    def post(self, request, *args, **kwargs):
        if 'slug' not in kwargs:
            raise Http404('Missing username')

        profile = self.model.objects.get(username=kwargs['slug'])
        if profile != self.request.user:
            raise Http404('Mismatch user')

        profile.first_name = self.request.POST.get('first-name', '')
        profile.last_name = self.request.POST.get('last-name', '')
        profile.organization = self.request.POST.get('organization', '')
        profile.email = self.request.POST.get('email', '')

        if not Profile.objects.filter(user=profile).exists():
            Profile.objects.create(user=profile)

        profile.user_profile.picture = self.request.FILES.get(
            'profile-picture', None
        )
        # profile.user_profile.title = self.request.POST.get('title', '')

        profile.user_profile.save()
        profile.save()

        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        return context
