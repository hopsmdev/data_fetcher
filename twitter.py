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


if __name__ == "__main__":

    credentials = CredentialsReader('credentials.ini')
    __api_key = credentials.twitter.api_key
    __api_secret_key = credentials.twitter.api_secret_key
    __access_token = credentials.twitter.access_token
    __access_secret = credentials.twitter.access_secret

    api = get_twitter_api(auth=get_0auth(
        __api_key, __api_secret_key, __access_token, __access_secret))


    def print_user_tweets(users):
        tweets = TweetsUser(api=api)
        for user in users:
            for tweet in tweets(user):
                print(user, tweet)

    users = ['gvanrossum', 'raymondh']
    #print_user_tweets(users)

    def print_hashtag_tweets(hashtags, since):
        tweets = TweetsHashtag(api=api)
        for hashtag in hashtags:
            for tweet in tweets(hashtag, since):
                print(hashtag, tweet)

    hashtags = ['#python']

    from datetime import date
    print_hashtag_tweets(hashtags, since=str(date.today()))