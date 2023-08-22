from django.conf import settings
from django.template import Context, Template
from django.test import TestCase


class SentryDsnTagTestCase(TestCase):

    def render_template(self, string, context=None):
        """Helper method to render templates"""
        context = context or {}
        t = Template(string)
        return t.render(Context(context))

    def test_sentry_dsn_template_tag(self):
        with self.settings(SENTRY_DSN="https://example.com/dsn"):
            rendered = self.render_template("{% load custom_tags %}{% sentry_dsn %}")
            self.assertEqual(rendered, "https://example.com/dsn")

        delattr(settings, "SENTRY_DSN")
        rendered = self.render_template("{% load custom_tags %}{% sentry_dsn %}")
        self.assertEqual(rendered, "")
