USERNAME_MAX_LENGTH = 32
USERNAME_REQUIRED_ERROR_MESSAGE = 'Please enter your username'
USERNAME_TOO_LONG_ERROR_MESSAGE = (
        f'Username can be at most {USERNAME_MAX_LENGTH} characters long')
USERNAME_NOT_AVAILABLE_ERROR_MESSAGE = 'User with that username already exists'

EMAIL_MAX_LENGTH = 64
EMAIL_REQUIRED_ERROR_MESSAGE = 'Please enter your email address'
EMAIL_INVALID_ERROR_MESSAGE = 'Please enter a valid email address'
EMAIL_TOO_LONG_ERROR_MESSAGE = (
        f'Email can be at most {EMAIL_MAX_LENGTH} characters long')
EMAIL_NOT_AVAILABLE_ERROR_MESSAGE = 'User with that email already exists'

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 32
PASSWORD_REQUIRED_ERROR_MESSAGE = 'Please enter your password'
PASSWORD_TOO_SHORT_ERROR_MESSAGE = (
        f'Password must be at least {PASSWORD_MIN_LENGTH} characters long')
PASSWORD_TOO_LONG_ERROR_MESSAGE = (
        f'Password can be at most {PASSWORD_MAX_LENGTH} characters long')
PASSWORDS_NOT_MATCH_ERROR_MESSAGE = "Passwords don't match"
