from django.test.testcases import TestCase
from frontend.forms import ContactUsForm


class TestContactUsForm(TestCase):

    def test_form(self):
        request = {
            'email': 'fan@kartoza.com',
            'message': 'Here',
            'subject': 'Test Subj',
            'name': 'Fan'
        }

        form = ContactUsForm()
        form._errors = {}
        form.cleaned_data = request
        form.clean()
        self.assertEquals(len(form._errors.keys()), 0)
