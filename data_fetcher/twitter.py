import os
import datetime
from collections import namedtuple

import tweepy

from data_fetcher.config_reader import ConfigReader


CREDENTIALS_INI = '../credentials.ini'


def get_0auth(api_key, api_secret_key, access_token, access_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_api(auth=None):
    """
    :param auth: tweepy.OAuthHandler object,
        if None we are using default auth obj
    :return:
    """
    if auth:
        _auth = auth
    else:
        _credentials = ConfigReader(CREDENTIALS_INI)
        print("--->", _credentials)
        _auth = get_0auth(
            api_key=_credentials.twitter.api_key,
            api_secret_key=_credentials.twitter.api_secret_key,
            access_token=_credentials.twitter.access_token,
            access_secret=_credentials.twitter.access_secret)
    return tweepy.API(_auth)


def get_twitter_data_config(
        data_configs="data_configs", config_ini="twitter.ini"):
    return ConfigReader(
        config_path=os.path.join(data_configs, config_ini)).twitter


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

    def __call__(self, user, number_of_tweets=20, since=None):
        """
        :param user: string, twitter screen name
        :param number_of_tweets: integer
        :param since: datetime.datetime type e.g
            datetime.datetime(2015, 12, 14, 16, 34, 33) or
            datetime.datetime.today()
        :return: tweepy Status object generator
        """
        if not number_of_tweets:
            number_of_tweets = 0
        for obj in tweepy.Cursor(
                self.api.user_timeline,
                screen_name=user).items(number_of_tweets):
            if since:
                if obj.created_at >= since:
                    yield self._tweet(str(obj.created_at), obj.text.encode('utf8'))
                else:
                    continue
            else:
                yield self._tweet(str(obj.created_at), obj.text.encode('utf8'))


class TweetsHashtag(Tweets):
    def __init__(self, api):
        self.api = api
        super(TweetsHashtag, self).__init__(api)

    def __call__(self, hashtag, since, number_of_tweets=20):
        search_params = {
            'q': hashtag, 'since': since, 'lang': 'en'}

        for obj in tweepy.Cursor(
                self.api.search, **search_params).items(number_of_tweets):
            yield self._tweet(str(obj.created_at), obj.text.encode('utf8'))


def get_hashtag_tweets(api, hashtag=None, since=None):
        _tweets = TweetsHashtag(api)
        for _tweet in _tweets(hashtag, since):
                yield _tweet


def get_user_tweets(api, user, number_of_tweets=None, since=None):
        _tweets = TweetsUser(api)
        for _tweet in _tweets(
                user=user, number_of_tweets=number_of_tweets, since=since):
            yield _tweet


if __name__ == "__main__":

    """
    twitter_data_config = get_twitter_data_config(
        data_configs="data_configs", config_ini="twitter.ini")

    users_to_observe = twitter_data_config.users.split(',')
    tags_to_observe = twitter_data_config.hashtags.split(',')
    """

    api = get_twitter_api()
    tweets = get_user_tweets(
        api, user="gvanrossum",
        number_of_tweets=0, since=datetime.datetime(2015, 12, 14, 16, 34, 33))

    for tweet in tweets:
        print(tweet)
