class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings
        getter = getattr(settings,
                         'DJANGO_BEHAVE_SETTING_GETTER',
                         lambda name, dflt: getattr(settings, name, dflt))
        return getter(self.prefix + name, dflt)

    # Before Django 1.7 LiveServerTestCase used to rely on the
    # staticfiles contrib app to get the static assets of the
    # application(s) under test transparently served at their
    # expected locations during the execution of these tests.

    # In Django 1.7 this dependency of core functionality on a
    # contrib application has been removed, because of which
    # LiveServerTestCase ability in this respect has been
    # retrofitted to simply publish the contents of the file
    # system under STATIC_ROOT at the STATIC_URL URL.
    @property
    def ENABLE_STATIC_TEST_SERVER(self):
        return self._setting("ENABLE_STATIC_TEST_SERVER", False)

    # Allows fixtures to be specified in the projects settings file
    # more modular design
    @property
    def FIXTURES(self):
        return self._setting("FIXTURES", '')

# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
import sys
app_settings = AppSettings('DJANGO_BEHAVE_')
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
