import re
from django.core.exceptions import ValidationError


class NumberValidator(object):
    """Checking if password contains a number character.

    """
    def validate(self, password, user=None):
        """Check password.

        :param
        password: Input password
        :type
        password: str
        """
        if not re.findall(r'\d', password):
            raise ValidationError(
                "The password must contain a numeric character",
                code='password_no_number',
            )

    def get_help_text(self):
        return "Numeric character"


class UppercaseValidator(object):
    """Checking if password contains an uppercase letter.

    """
    def validate(self, password, user=None):
        """Check password.

        :param
        password: Input password
        :type
        password: str
        """

        if not re.findall('[A-Z]', password):
            raise ValidationError(
                "The password must contain an uppercase letter",
                code='password_no_upper',
            )

    def get_help_text(self):
        return "Uppercase letter"


class SymbolValidator(object):
    """Checking if password contains a special character.

    """
    def validate(self, password, user=None):
        """Check password.

        :param
        password: Input password
        :type
        password: str
        """
        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                "The password must contain a special character.",
                code='password_no_symbol',
            )

    def get_help_text(self):
        return "Special character (@#%;)"
