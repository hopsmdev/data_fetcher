import os
import unittest

import tweepy
from data_fetcher.config_reader import ConfigReader

from data_fetcher import twitter
from data_fetcher.tests import CURRENT_DIR

CREDENTIALS_INI = os.path.abspath(os.path.join(CURRENT_DIR, 'test_credentials.ini'))


class ConfigReaderTest(unittest.TestCase):

    def setUp(self):
        self.credentials_reader = ConfigReader(
            config_path=CREDENTIALS_INI)

    def test_twitter(self):
        self.assertEqual(
            self.credentials_reader.twitter.api_key, 'secretkey')
        self.assertEqual(
            self.credentials_reader.twitter.api_secret_key, 'secretkey')
        self.assertEqual(
            self.credentials_reader.twitter.access_token, 'secretkey')
        self.assertEqual(
            self.credentials_reader.twitter.access_secret, 'secretkey')

    def test_attr_noexist(self):
        self.assertEqual(self.credentials_reader.noexists, None)


class GetTweetsTest(unittest.TestCase):

    def setUp(self):
        credentials = ConfigReader(config_path=CREDENTIALS_INI)
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
        self.assertIsInstance(auth, tweepy.auth.OAuthHandler)


if __name__ == "__main__":
    unittest.main()