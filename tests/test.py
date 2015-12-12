import unittest
from credentials_reader import CredentialsReader


class CredentialsReaderTest(unittest.TestCase):

    def setUp(self):
        credentials_path = '../credentials.ini'
        self.credentials_reader = CredentialsReader(credentials_path)

    def test_twitter(self):
        print(self.credentials_reader.twitter.api_key)
        print(self.credentials_reader.twitter.api_secret_key)


if __name__ == "__main__":
    unittest.main()