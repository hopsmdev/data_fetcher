import configparser
from collections import namedtuple


class ConfigReader(object):
    """
    How to use:
    credentials_reader = ConfigReader(config_path)
    credentials_reader.twitter.api_key

    Attributes for object generated according to sections
    in credentials.ini file - you should add attribute name
    to __attrs__ list.
    """

    __attrs__ = ['twitter']

    def __init__(self, config_path='../credentials.ini'):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def __getattr__(self, item):
        if item in self.__attrs__:
            _section = item
            try:
                _items = self.config[_section].items()
                _attribute = namedtuple(
                    _section, self.config.options(_section))
                return _attribute(**{key: value for (key, value) in _items})
            except configparser.NoSectionError:
                raise RuntimeError(
                    'Cannot find {} section in {}'.format(
                        _section, self.config_path))