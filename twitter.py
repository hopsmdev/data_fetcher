import tweepy
from credentials_reader import CredentialsReader


def get_0auth(api_key, api_secret_key, access_token, access_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_api(auth):
    return tweepy.API(auth)


credentials = CredentialsReader('credentials.ini')
__api_key = credentials.twitter.api_key
__api_secret_key = credentials.twitter.api_secret_key
__access_token = credentials.twitter.access_token
__access_secret = credentials.twitter.access_secret

api = get_twitter_api(auth=get_0auth(
    __api_key, __api_secret_key, __access_token, __access_secret))


screen_name = 'gvanrossum'
tweets = api.user_timeline(screen_name=screen_name, count=200)
for tweet in tweets:
    print((str(tweet.created_at), tweet.text))