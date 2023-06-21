import re
from django.core.exceptions import ValidationError


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                "The password must contain a numeric character",
                code='password_no_number',
            )

    def get_help_text(self):
        return "Numeric caracter"


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                "The password must contain an uppercase letter",
                code='password_no_upper',
            )

    def get_help_text(self):
        return "Uppercase letter"


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                "The password must contain a special character",
                code='password_no_symbol',
            )

    def get_help_text(self):
        return "Special character (@#%;)"
        