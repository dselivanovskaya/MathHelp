''' These constants are used in test cases. '''


class TestUser:
    ''' Class for storing test users credentials.  '''

    def __init__(self, full_name: str, email: str, username: str, passwd: str):
        self.full_name = full_name
        self.email = email
        self.username = username
        self.password = passwd


USER1 = TestUser('John Smith', 'john@gmail.com', 'john', 'johny_123')
USER2 = TestUser('Alice Brooks', 'alice@gmail.com', 'alice', 'alicia_123')
