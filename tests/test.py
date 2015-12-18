import unittest
import twitter
from credentials_reader import CredentialsReader

class CredentialsReaderTest(unittest.TestCase):

    def setUp(self):
        credentials_path = '../credentials.ini'
        self.credentials_reader = CredentialsReader(credentials_path)

    def test_twitter(self):
        print(self.credentials_reader.twitter.api_key)
        print(self.credentials_reader.twitter.api_secret_key)

    def test_attr_noexist(self):
        self.assertEqual(self.credentials_reader.noexists, None)


class GetTweetsTest(unittest.TestCase):

    def setUp(self):
        credentials = CredentialsReader()
        self.__api_key = credentials.twitter.api_key
        self.__api_secret_key = credentials.twitter.api_secret_key
        self.__access_token = credentials.twitter.access_token
        self.__access_secret = credentials.twitter.access_secret

    def test_oauth(self):
        auth = twitter.get_0auth(
            self.__api_key,
            self.__api_secret_key,
            self.__access_token,
            self.__access_secret)


if __name__ == "__main__":
    unittest.main()