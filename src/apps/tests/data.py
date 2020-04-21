''' These constants are used in test cases. '''

from django.contrib.auth import get_user_model


class TestUser:
    ''' Class for storing test users credentials.  '''

    def __init__(self, first_name, last_name, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password

    def create_in_db(self):
        return get_user_model().objects.create_user(
            username=self.username, email=self.email, password=self.password,
            first_name=self.first_name, last_name=self.last_name,
        )


USER1 = TestUser('John', 'Smith', 'john@gmail.com', 'john', 'johny_123')
USER2 = TestUser('Alice', 'Brooks', 'alice@gmail.com', 'alice', 'alicia_123')
