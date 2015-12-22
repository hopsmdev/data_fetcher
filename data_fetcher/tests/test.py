import os
import unittest
from collections import namedtuple

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


class TestTwitterCredentials(unittest.TestCase):

    def setUp(self):
        self.credentials = {
            'access_token_secret': 'secretkey',
            'access_token': 'secretkey',
            'api_secret_key': 'secretkey',
            'api_key': 'secretkey'
        }

        os.environ.update({
            'TWITTER_API_KEY': 'secretkey',
            'TWITTER_API_SECRET': 'secretkey',
            'TWITTER_ACCESS_TOKEN': 'secretkey',
            'TWITTER_ACCESS_SECRET': 'secretkey'
        })

    def test_get_fromfile_credentials(self):
        fromfile_credentials = twitter.get_fromfile_credentials(CREDENTIALS_INI)
        self.assertDictEqual(fromfile_credentials, self.credentials)

    def test_get_env_credentials(self):
        env_credentials = twitter.get_env_credentials()
        self.assertDictEqual(env_credentials, self.credentials)

    def test_get_0auth_with_credentials_ini(self):
        auth = twitter.get_0auth(credentials_ini=CREDENTIALS_INI)
        self.assertIsInstance(auth, tweepy.auth.OAuthHandler)


class TwitterTest(unittest.TestCase):

    def setUp(self):
        self.auth = twitter.get_0auth(credentials_ini=CREDENTIALS_INI)

    def test_get_twitter_api(self):
        self.assertIsInstance(twitter.get_twitter_api(auth=self.auth), tweepy.API)

if __name__ == "__main__":
    unittest.main()