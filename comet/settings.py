import os
import json

from appdirs import user_config_dir

class Settings:
    """Storing persistent application settings on any platform.

    >>> with Settings('HEPHY', 'comet') as settings:
    ...    settings['app'] = {'name': 'My App', users=['Monty', 'John'])
    ...    name = settings.get('app').get('name')

    """

    settings_filename = 'settings.json'
    """Filename used to store settings in JSON format."""

    def __init__(self, organization, application, persistent=True):
        self.__application = application
        self.__organization = organization
        self.__persistent = persistent
        self.__path = user_config_dir(appname=application, appauthor=organization)
        self.__filename = os.path.join(self.__path, self.settings_filename)
        self.__settings = {}

    @property
    def organization(self):
        return self.__organization

    @property
    def application(self):
        return self.__application

    def __enter__(self):
        """Read application settings from filesystem (if existing)."""
        if os.path.isfile(self.__filename):
            with open(self.__filename, 'r') as f:
                self.__settings = json.load(f)
        return self.__settings

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Write application settings to filesystem."""
        if self.__persistent:
            if not os.path.exists(self.__path):
                os.makedirs(self.__path)
            with open(self.__filename, 'w') as f:
                json.dump(self.__settings, f)
