from django.core.exceptions import ValidationError


class CustomPasswordValidator:

    def __init__(self):
        self.special_characters = '[~\!@#\$%\^&\*\(\)_\+{}":;\'\[\]]'

    def validate(self, password: str, user=None):

        # Check for at least one digit.
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least 1 digit.')

        # Check for at least one special character.
        if not any(char in self.special_characters for char in password):
            raise ValidationError(
                 'Password must contain at least 1 of these characters '
                f'{self.special_characters}.'
            )

    def get_help_text(self):
        return (
            'Your password must containt at least 1 digit and 1 of these '
            f'characters {self.special_characters}.'
        )
