
from django.core.exceptions import ValidationError

class CustomPasswordValidator:

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        # check for digit
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least 1 digit.'))
        # check for letter
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('Password must contain at least 1 letter.'))
        # check for special character
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(char in special_characters for char in password):
            raise ValidationError(_('Password must contain at least 1 letter.'))

    def get_help_text(self):
        return "BEEEEEEEE"
