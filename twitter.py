import os
import configparser
from collections import namedtuple
from credentials_reader import CredentialsReader

import tweepy


def get_0auth(api_key, api_secret_key, access_token, access_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_api(auth):
        return tweepy.API(auth)


class Tweets(object):
    def __init__(self, api):
        self.api = api
        self._tweet = namedtuple('tweets', ['created_at', 'text'])

    def __str__(self):
        return "{date}: {text}".format(
            date=self._tweet.created_at, text=self._tweet.text)


class TweetsUser(Tweets):
    def __init__(self, api):
        self.api = api
        super(TweetsUser, self).__init__(api)

    def __call__(self, user_name):
        for obj in self.api.user_timeline(screen_name=user_name, count=200):
            yield self._tweet(str(obj.created_at), obj.text.encode('utf8'))


class TweetsHashtag(Tweets):
    def __init__(self, api):
        self.api = api
        super(TweetsHashtag, self).__init__(api)

    def __call__(self, hashtag, since):
        search_params = {
            'q': hashtag, 'since': since, 'lang': 'en'}

        for obj in tweepy.Cursor(self.api.search, **search_params).items(30):
            yield self._tweet(str(obj.created_at), obj.text.encode('utf8'))


class TwitterDataConfig(object):
    def __init__(self, data_configs="data_configs", config_ini="twitter.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(data_configs, config_ini))

    @property
    def twitter(self):
        _twitter_section = 'twitter'
        try:
            _items = self.config[_twitter_section].items()
            _twitter = namedtuple(
                'twitter', self.config.options(_twitter_section))
            return _twitter(**{key: value for (key, value) in _items})
        except configparser.NoSectionError:
            raise RuntimeError('Cannot find twitter data configuration in twitter.ini')


class TwitterDataFetcher(object):
    def __init__(self, twitter_config_obj, auth_obj=None):
        self.users_to_observe = twitter_config_obj.users.split(',')
        self.tags_to_observe = twitter_config_obj.hashtags.split(',')

        if auth_obj:
            self.auth = auth_obj
        else:
            self.auth = self.default_auth

        self.api = get_twitter_api(self.auth)

    @property
    def default_auth(self):
        _credentials = CredentialsReader('credentials.ini')
        return get_0auth(
            api_key=_credentials.twitter.api_key,
            api_secret_key=_credentials.twitter.api_secret_key,
            access_token=_credentials.twitter.access_token,
            access_secret=_credentials.twitter.access_secret)

    def get_hashtag_tweets(self, hashtags=None, since=None):
        tweets = TweetsHashtag(api=self.api)
        if self.tags_to_observe:
            hashtags = self.tags_to_observe
        for hashtag in hashtags:
            for _tweet in tweets(hashtag, since):
                yield _tweet

    def get_user_tweets(self, users=None):
        tweets = TweetsUser(api=self.api)
        if self.users_to_observe:
            users = self.users_to_observe
        for user in users:
            for _tweet in tweets(user):
                yield _tweet


if __name__ == "__main__":

    twitter_data_config = TwitterDataConfig().twitter
    twitter_data_fetcher = TwitterDataFetcher(twitter_data_config)

    from datetime import date
    tweets = twitter_data_fetcher.get_hashtag_tweets(since=str(date.today()))
    for tweet in tweets:
        print(tweet)