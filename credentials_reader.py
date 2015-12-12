import configparser
from collections import namedtuple


class CredentialsReader(object):
    def __init__(self, credentials_path):
        self.config = configparser.ConfigParser()
        self.config.read(credentials_path)

    @property
    def twitter(self):
        _twitter_section = 'twitter'
        try:
            _items = self.config[_twitter_section].items()
            twitter = namedtuple(
                'twitter', self.config.options(_twitter_section))
            return twitter(**{key: value for (key, value) in _items})
        except configparser.NoSectionError:
            raise RuntimeError('Cannot find twitter credentials in credentials.ini')

