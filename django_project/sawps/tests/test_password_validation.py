from django.test import TestCase
from django.core.exceptions import ValidationError

from sawps.password_validation import (
    NumberValidator,
    UppercaseValidator,
    SymbolValidator
)
import logging

logger = logging.getLogger(__name__)


class TestPasswordValidator(TestCase):
    """Test password validator.

    """

    def test_password_number(self):
        """Test password validator contains number character.

        """
        password = 'A!D$!$Qcc'
        with self.assertRaises(ValidationError):
            NumberValidator().validate(password, user=None)

    def test_password_uppercase(self):
        """Test password validator contains uppercase character.

        """
        password = 'a22!a$!$qcc'
        with self.assertRaises(ValidationError):
            UppercaseValidator().validate(password, user=None)

    def test_password_special(self):
        """Test password validator contains special character.

        """
        password = 'a22aqcc'
        with self.assertRaises(ValidationError):
            SymbolValidator().validate(password, user=None)