from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def sentry_dsn():
    return getattr(settings, "SENTRY_DSN", "")
