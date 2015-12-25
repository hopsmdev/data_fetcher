import os
import configparser
from collections import namedtuple
from data_fetcher import CURRENT_DIR

CREDENTIALS_INI = os.path.abspath(
    os.path.join(CURRENT_DIR, os.pardir, 'credentials.ini'))


def get_config_parser(config_file=None):
    config_parser = configparser.ConfigParser()
    parsed_config_files = config_parser.read(config_file)
    if not parsed_config_files:
        raise ConfigReaderException('Cannot find configuration file')
    return config_parser


class ConfigReaderException(Exception):
    pass


class ConfigReader(object):
    """
    How to use:
    credentials_reader = ConfigReader(config_path)
    credentials_reader.twitter.api_key

    Attributes for object generated according to sections
    in credentials.ini file - you should add attribute name
    to sections list.
    """

    def __init__(self, config_file=CREDENTIALS_INI):
        self.config_parser = get_config_parser(config_file)
        self.config_file = config_file
        self.sections = self.config_parser.sections()

    def __getattr__(self, section):
        if section not in self.sections:
            return
        try:
            items = self.config_parser[section].items()
            _attribute = namedtuple(
                section, self.config_parser.options(section))
            return _attribute(**{key: value for (key, value) in items})
        except configparser.NoSectionError:
            msg = 'Cannot find {} section in {}'.format(
                section, self.config_file)
            raise ConfigReaderException(msg)