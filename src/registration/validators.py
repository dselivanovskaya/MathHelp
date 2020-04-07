from django.core.exceptions import ValidationError


class CustomPasswordValidator:

    def __init__(self):
        self.special_characters = '[~\!@#\$%\^&\*\(\)_\+{}":;\'\[\]]'

    def validate(self, password: str, user=None):
        # Check for at least one digit.
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least 1 digit.')

        # Check for at least one uppercase letter.
        if not any(char.isupper() for char in password):
            raise ValidationError(
                'Password must contain at least 1 uppercase letter.'
            )

        # Check for at least one lowercase letter.
        if not any(char.islower() for char in password):
            raise ValidationError(
                'Password must contain at least 1 lowercase letter.'
            )

        # Check for at least one special character.
        if not any(char in self.special_characters for char in password):
            raise ValidationError(
                'Password must contain at least 1 special character.'
            )

    def get_help_text(self):
        return (
            'Your password must containt at least 1 digit, 1 uppercase '
            'letter, 1 lowercase letter and 1 special character.'
        )
