from django.core.exceptions import ValidationError


class CustomPasswordValidator:

    special_chars = '~ ! @  # $ % ^ & * (  ) _ + {  } " : ; \' [ ] '

    error_messages = {
        'digit': 'Password must contain at least 1 digit.',
        'special_char': (
            'Password must contain at least 1 of '
            f'these characters: {special_chars}.'
        )
    }

    def validate(self, password: str, user=None):
        # Check for at least one digit.
        if not any(char.isdigit() for char in password):
            raise ValidationError(self.error_messages['digit'])

        # Check for at least one special character.
        if not any(char in self.special_chars for char in password):
            raise ValidationError(self.error_messages['special_char'])

    def get_help_text(self):
        return (
            f'Your {self.error_messages["digit"].lower()} and '
            f'1 of these characters: {self.special_chars}.'
        )
