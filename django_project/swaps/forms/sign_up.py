from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=150,
        label='First Name',
        required=True)
    last_name = forms.CharField(
        max_length=150,
        label='Last Name',
        required=True
    )
    organisation = forms.CharField(
        max_length=100,
        label='Organisation or Entreprise name',
        required=True
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label='Role',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    field_order = ['first_name', 'last_name' , 'email', 'organisation', 'group', 'password']

    def custom_signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.organisation = self.cleaned_data['organisation']
        try:
            user.groups.set(Group.objects.get(id=self.cleaned_data['group']))
        except:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
