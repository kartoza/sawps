import logging
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from stakeholder.models import UserProfile, UserRoleType, UserTitle

logger = logging.getLogger(__name__)


class ProfileView(DetailView):
    template_name = 'profile.html'
    model = get_user_model()
    slug_field = 'username'

    def post(self, request, *args, **kwargs):
        if 'slug' not in kwargs:
            raise Http404('Missing username')

        profile = self.model.objects.get(username=kwargs['slug'])
        if profile != self.request.user:
            raise Http404('Mismatch user')

        if self.request.POST.get('first-name', ''):
            profile.first_name = self.request.POST.get('first-name', '')
        if self.request.POST.get('last-name', ''):
            profile.last_name = self.request.POST.get('last-name', '')

        if self.request.POST.get('email', ''):
            profile.email = self.request.POST.get('email', '')

        if not UserProfile.objects.filter(user=profile).exists():
            UserProfile.objects.create(
                user=profile,
            )

        if self.request.FILES.get('profile-picture', None):
            profile.user_profile.picture = self.request.FILES.get(
                'profile-picture', None
            )
        if self.request.POST.get('title', ''):
            title = UserTitle.objects.get(
                id=self.request.POST.get('title', ''))
            profile.user_profile.title_id = title
        if self.request.POST.get('role', ''):
            role = UserRoleType.objects.get(
                id=self.request.POST.get('role', '')
            )
            profile.user_profile.user_role_type_id = role

        profile.user_profile.save()
        profile.save()

        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['titles'] = UserTitle.objects.all()
        context['roles'] = UserRoleType.objects.all()

        return context
