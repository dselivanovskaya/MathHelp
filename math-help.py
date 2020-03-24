import json                      # To parse response
import urllib.request as urlreq  # To send a request

from typing import Dict, List


HOST = '127.0.0.1'
PORT = 8000
SUCCESS = 200

MALE, FEMALE = 1, 2

class Extractor:

    def __init__(self, data: List[dict]):
        self.data = data

    def get_user_count(self) -> int:
        ''' Return number of registered users. '''
        return len(self.data)

    def get_usernames(self) -> List[str]:
        ''' Return a list of usernames. '''
        return [user['username'] for user in self.data]

    def get_user_emails(self) -> List[str]:
        ''' Return a list of user-emails. '''
        return [user['email'] for user in self.data]

    def get_male_count(self) -> int:
        ''' Return number of male users. '''
        return len([user['gender'] for user in self.data
                    if user['gender'] == MALE])

    def get_female_count(self) -> int:
        ''' Return number of female users. '''
        return len([user['gender'] for user in self.data
                    if user['gender'] == FEMALE])


def main():
    response = urlreq.urlopen(url=f'http://{HOST}:{PORT}/api/users/')
    if response.getcode() == SUCCESS:
        extractor = Extractor(json.loads(response.read()))
        print(f'Total: {extractor.get_user_count()}')
        print(extractor.get_usernames())
        print(extractor.get_user_emails())
        print(f'Males: {extractor.get_male_count()}')
        print(f'Females: {extractor.get_female_count()}')


if __name__ == '__main__':
    main()
