import os
import datetime
from functools import partial
from collections import namedtuple

import tweepy

# TODO fix relative imports

from data_fetcher import CURRENT_DIR
from data_fetcher import logger
from data_fetcher.config_reader import ConfigReader, ConfigReaderException


MAX_TWEETS_NUMBER = 1000
CREDENTIALS_INI = os.path.abspath(
    os.path.join(CURRENT_DIR, os.pardir, 'credentials.ini'))


def get_tweepy_cursor(method, *args, **kwargs):
    return tweepy.Cursor(method, *args, **kwargs)


class Tweets(object):
    def __init__(self, api):
        self.api = api
        self._tweet = namedtuple('tweets', ['created_at', 'text'])

    def __str__(self):
        return "{date}: {text}".format(
            date=self._tweet.created_at, text=self._tweet.text)


class TweetsUser(Tweets):
    def __init__(self, api):
        self.cursor = partial(tweepy.Cursor, api.user_timeline)
        super(TweetsUser, self).__init__(api)

    def get_tweets(self, user, number_of_tweets, since):
        if since:
            return (tweet for tweet in
                    self.cursor(screen_name=user).items(number_of_tweets)
                    if tweet.created_at >= since)
        else:
            return self.cursor(screen_name=user).items(number_of_tweets)

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
            number_of_tweets = MAX_TWEETS_NUMBER

        for tweet in self.get_tweets(user, number_of_tweets, since):
            yield self._tweet(str(tweet.created_at), tweet.text.encode('utf8'))


class TweetsQuery(Tweets):
    def __init__(self, api):
        self.cursor = partial(tweepy.Cursor, api.search)
        super(TweetsQuery, self).__init__(api)

    def get_tweets(self, query, number_of_tweets, since):
        if since:
            return (tweet for tweet in
                    self.cursor(q=query).items(number_of_tweets)
                    if tweet.created_at >= since)
        else:
            return self.cursor(q=query).items(number_of_tweets)

    def __call__(self, query, number_of_tweets=20, since=None):

        if not number_of_tweets:
            number_of_tweets = MAX_TWEETS_NUMBER

        for obj in self.get_tweets(query, number_of_tweets, since):
            yield self._tweet(str(obj.created_at), obj.text.encode('utf8'))


def get_env_credentials():
    logger.info("Get Twitter credentials from ENV")
    return {
        'api_key': os.environ.get('TWITTER_API_KEY', ''),
        'api_secret_key': os.environ.get('TWITTER_API_SECRET', ''),
        'access_token': os.environ.get('TWITTER_ACCESS_TOKEN', ''),
        'access_token_secret': os.environ.get('TWITTER_ACCESS_SECRET', '')
    }


def get_fromfile_credentials(credentials_ini=None):

    if not credentials_ini:
        credentials_ini = CREDENTIALS_INI

    logger.info("Get Twitter credentials from {}".format(credentials_ini))
    try:
        credentials_config = ConfigReader(credentials_ini)
    except ConfigReaderException:
        return False

    return {
        'api_key': credentials_config.twitter.api_key,
        'api_secret_key': credentials_config.twitter.api_secret_key,
        'access_token': credentials_config.twitter.access_token,
        'access_token_secret': credentials_config.twitter.access_secret
     }


def get_twitter_credentials(credentials_ini=None):

    oauth = get_fromfile_credentials(credentials_ini) or get_env_credentials()
    credentials = namedtuple('credentials', oauth.keys())
    return credentials(**oauth)


def get_0auth(credentials_ini=None):

    _cred = get_twitter_credentials(credentials_ini)

    auth = tweepy.OAuthHandler(_cred.api_key, _cred.api_secret_key)
    auth.set_access_token(_cred.access_token, _cred.access_token_secret)
    return auth


def get_twitter_api(auth=None):
    """
    :param auth: tweepy.OAuthHandler object,
        if None we are using default auth obj
    :return:
    """
    return tweepy.API(auth)


def get_twitter_data_config(
        data_configs="data_configs", config_ini="twitter.ini"):
    return ConfigReader(
        config_path=os.path.join(data_configs, config_ini)).twitter


def get_hashtag_tweets(api, query=None, number_of_tweets=None, since=None):
        _tweets = TweetsQuery(api)
        for _tweet in _tweets(
                query=query, number_of_tweets=number_of_tweets, since=since):
            yield _tweet


def get_user_tweets(api, user, number_of_tweets=None, since=None):
        _tweets = TweetsUser(api)
        for _tweet in _tweets(
                user=user, number_of_tweets=number_of_tweets, since=since):
            yield _tweet


def main():
    auth = get_0auth()
    tweets = get_user_tweets(
        api=get_twitter_api(auth),
        user="gvanrossum",
        number_of_tweets=5,
        since=datetime.datetime(2015, 12, 14, 16, 34, 33))

    for tweet in tweets:
        print(tweet)

    tweets2 = get_hashtag_tweets(
        api=get_twitter_api(auth),
        query="#python",
        number_of_tweets=20,
        since=datetime.datetime(2015, 12, 26, 16, 34, 33))

    print(tweets2)
    for tweet in tweets2:
        print(tweet)

if __name__ == "__main__":

    """
    twitter_data_config = get_twitter_data_config(
        data_configs="data_configs", config_ini="twitter.ini")

    users_to_observe = twitter_data_config.users.split(',')
    tags_to_observe = twitter_data_config.hashtags.split(',')
    """

    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print(end - start)