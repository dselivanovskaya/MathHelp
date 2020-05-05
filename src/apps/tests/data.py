from django.contrib.auth import get_user_model


class TestUser:
    ''' Class for storing test users credentials.  '''

    def __init__(self, username, email, password, first_name='', last_name='',
                 gender='M', age=0, is_superuser=False):
        # User data
        self.username = username
        self.email = email
        self.password = password
        self.is_superuser = is_superuser
        # Profile data
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age

    def create(self):
        if self.is_superuser:
            create_user_function = get_user_model().objects.create_superuser
        else:
            create_user_function = get_user_model().objects.create_user

        user = create_user_function(
            username=self.username, email=self.email, password=self.password
        )

        user.profile.first_name = self.first_name
        user.profile.last_name = self.last_name
        user.profile.gender = self.gender
        user.profile.age = self.age

        return user


MALE_USER = TestUser(
    'john',  'john@gmail.com',  'johny_123', 'John', 'Smith', 'M', 20
)

FEMALE_USER = TestUser(
    'alice', 'alice@gmail.com', 'alicia_123', 'Alice', 'Michaels', 'F', 22
)

SUPER_USER = TestUser(
    'admin', 'admin@gmail.com', 'adminn_123', is_superuser=True
)
