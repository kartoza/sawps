from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(required=True, max_length=512)
    email = forms.EmailField(required=True)

    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control"})
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': "form-control",'style':"height:80px"}),
        required=True
    )

    copy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': "form-check-input"})
    )

    def clean(self):
        cleaned_data = super(ContactUsForm, self).clean()
        return cleaned_data