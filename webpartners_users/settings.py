from __future__ import unicode_literals

from django.conf import settings

DEFAULTS = {
    'PASSWORD_VALIDATION': {
        'MIN_LENGTH': None,
        'AT_LEAST_ONE_NUMBER': False,
        'NUMERIC_DISALLOWED': False,
    }
}


class Settings(object):
    """
    A settings object, that allows API settings to be accessed as properties.
    """
    def __init__(self, key, defaults=None):
        self.key = key
        self.defaults = defaults or DEFAULTS

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid API setting: '%s'" % attr)

        user_settings = getattr(settings, self.key, {})
        try:
            # Check if present in user settings
            val = user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        #setattr(self, attr, val)
        return val


package_settings = Settings('WEBPARTNERS_USERS')
