"""Django test runner which uses behave for BDD tests.
"""

from optparse import make_option
from os.path import dirname, abspath, basename, join, isdir

try:
    from django.test.runner import DiscoverRunner as BaseRunner
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner as BaseRunner

try:
    # This is for Django 1.7 where StaticLiveServerTestCase is needed for
    # static files to "just work"
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase as LiveServerTestCase
except ImportError:
    from django.test import LiveServerTestCase

try:
    # since Django 1.7
    from django.apps import apps


    def get_app(label):
        if label.endswith('/'):
            print("Removing trailing slash of label: %s" % label)
            label = label[:-1]

        appconfig = apps.get_app_config(label)
        return appconfig.models_module or appconfig.module

except ImportError:
    from django.db.models import get_app

import unittest
from django.utils import six
from django.utils.six.moves import xrange
from django.conf import settings

from behave.configuration import Configuration, ConfigError, options
from behave.runner import Runner as BehaveRunner
from behave.parser import ParserError
from behave.formatter.ansi_escapes import escapes

import sys


def get_app_dir(app_module):
    app_dir = dirname(app_module.__file__)
    if basename(app_dir) == 'models':
        app_dir = abspath(join(app_dir, '..'))
    return app_dir


def get_features(app_module):
    app_dir = get_app_dir(app_module)
    features_dir = abspath(join(app_dir, 'features'))
    if isdir(features_dir):
        return features_dir
    else:
        return None


# Get Behave command line options and add our own
def get_options():
    option_list = (
        make_option("--behave_browser",
                    action="store",
                    dest="browser",
                    help="Specify the browser to use for testing",
                    ),
    )

    option_info = {"--behave_browser": True}

    for fixed, keywords in options:
        # Look for the long version of this option
        long_option = None
        for option in fixed:
            if option.startswith("--"):
                long_option = option
                break

        # Only deal with those options that have a long version
        if long_option:
            # remove function types, as they are not compatible with optparse
            if hasattr(keywords.get('type'), '__call__'):
                del keywords['type']

            # Remove 'config_help' as that's not a valid optparse keyword
            if "config_help" in keywords:
                keywords.pop("config_help")

            name = "--behave_" + long_option[2:]

            option_list = option_list + \
                          (make_option(name, **keywords),)

            # Need to store a little info about the Behave option so that we
            # can deal with it later.  'has_arg' refers to if the option has
            # an argument.  A boolean option, for example, would NOT have an
            # argument.
            action = keywords.get("action", "store")
            if action == "store" or action == "append":
                has_arg = True
            else:
                has_arg = False

            option_info.update({name: has_arg})

    return (option_list, option_info)


# Parse options that came in.  Deal with ours, create an ARGV for Behave with
# it's options
def parse_argv(argv, option_info):
    behave_options = option_info.keys()
    new_argv = ["behave", ]
    our_opts = {"browser": None}

    for index in xrange(len(argv)):  # using range to have compatybility with Py3
        # If it's a behave option AND is the long version (starts with '--'),
        # then proceed to save the information.  If it's not a behave option
        # (which means it's most likely a Django test option), we ignore it.
        if argv[index] in behave_options and argv[index].startswith("--"):
            if argv[index] == "--behave_browser":
                our_opts["browser"] = argv[index + 1]
                index += 1  # Skip past browser option arg
            else:
                # Convert to Behave option
                new_argv.append("--" + argv[index][9:])

                # Add option argument if there is one
                if option_info[argv[index]] == True:
                    new_argv.append(argv[index + 1])
                    index += 1  # Skip past option arg

    return (new_argv, our_opts)


class DjangoBehaveTestCase(LiveServerTestCase):
    def __init__(self, **kwargs):
        self.features_dir = kwargs.pop('features_dir')
        self.option_info = kwargs.pop('option_info')
        super(DjangoBehaveTestCase, self).__init__(**kwargs)

    def __hash__(self):
        return hash((type(self), self._testMethodName, self.features_dir))

    def get_features_dir(self):
        if isinstance(self.features_dir, six.string_types):
            return [self.features_dir]
        return self.features_dir

    def setUp(self):
        self.setupBehave()

    def setupBehave(self):
        # Create a sys.argv suitable for Behave to parse
        old_argv = sys.argv
        (sys.argv, our_opts) = parse_argv(old_argv, self.option_info)
        self.behave_config = Configuration()
        sys.argv = old_argv
        self.behave_config.browser = our_opts["browser"]

        self.behave_config.server_url = self.live_server_url  # property of LiveServerTestCase
        self.behave_config.paths = self.get_features_dir()
        self.behave_config.format = self.behave_config.format if self.behave_config.format else ['pretty']
        # disable these in case you want to add set_trace in the tests you're developing
        self.behave_config.stdout_capture = \
            self.behave_config.stdout_capture if self.behave_config.stdout_capture else False
        self.behave_config.stderr_capture = \
            self.behave_config.stderr_capture if self.behave_config.stderr_capture else False

    def runTest(self, result=None):
        # run behave on a single directory

        # from behave/__main__.py
        # stream = self.behave_config.output
        runner = BehaveRunner(self.behave_config)
        failed = runner.run()

        try:
            undefined_steps = runner.undefined_steps
        except AttributeError:
            undefined_steps = runner.undefined

        if self.behave_config.show_snippets and undefined_steps:
            msg = u"\nYou can implement step definitions for undefined steps with "
            msg += u"these snippets:\n\n"
            printed = set()

            if sys.version_info[0] == 3:
                string_prefix = "('"
            else:
                string_prefix = u"(u'"

            for step in set(undefined_steps):
                if step in printed:
                    continue
                printed.add(step)

                msg += u"@" + step.step_type + string_prefix + step.name + u"')\n"
                msg += u"def impl(context):\n"
                msg += u"    assert False\n\n"

            sys.stderr.write(escapes['undefined'] + msg + escapes['reset'])
            sys.stderr.flush()

        if failed:
            raise AssertionError('There were behave failures, see output above')
            # end of from behave/__main__.py


class DjangoBehaveTestSuiteRunner(BaseRunner):
    @classmethod
    def add_arguments(cls, parser):
        # Set up to accept all of Behave's command line options and our own.  In
        # order to NOT conflict with Django's test command, we'll start all options
        # with the prefix "--behave_" (we'll only do the long version of an option).
        super(DjangoBehaveTestSuiteRunner, cls).add_arguments(parser)
        option_list, cls.option_info = get_options()

        for option in option_list:
            parser.add_argument(*option._long_opts, action=option.action, dest=option.dest, help=option.help)

    def make_bdd_test_suite(self, features_dir):
        return DjangoBehaveTestCase(features_dir=features_dir, option_info=self.option_info)

    def get_features_dirs(self, test_labels):
        if not test_labels:
            test_labels = settings.INSTALLED_APPS

        for label in test_labels:
            if '.' in label:
                short_label = label.split('.')[-1]
            else:
                short_label = None

            app = get_app(short_label or label)

            features_dir = get_features(app)
            if features_dir is not None:
                yield features_dir

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        extra_tests = extra_tests or []

        for features_dir in self.get_features_dirs(test_labels):
            extra_tests.append(self.make_bdd_test_suite(features_dir))

        return super(DjangoBehaveTestSuiteRunner, self
                     ).build_suite(test_labels, extra_tests, **kwargs)


if not hasattr(BaseRunner, 'add_arguments'):
    option_list, option_info = get_options()
    DjangoBehaveTestSuiteRunner.option_list = option_list
    DjangoBehaveTestSuiteRunner.option_info = option_info


class DjangoBehaveOnlyTestSuiteRunner(DjangoBehaveTestSuiteRunner):
    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = unittest.TestSuite()

        for features_dir in self.get_features_dirs(test_labels):
            suite.addTest(self.make_bdd_test_suite(features_dir))

        return reorder_suite(suite, (unittest.TestCase,))


def reorder_suite(suite, classes):
    """
    Reorders a test suite by test type.

    `classes` is a sequence of types

    All tests of type classes[0] are placed first, then tests of type
    classes[1], etc. Tests with no match in classes are placed last.
    """
    class_count = len(classes)
    bins = [unittest.TestSuite() for i in range(class_count+1)]
    partition_suite(suite, classes, bins)
    for i in range(class_count):
        bins[0].addTests(bins[i+1])
    return bins[0]


def partition_suite(suite, classes, bins):
    """
    Partitions a test suite by test type.

    classes is a sequence of types
    bins is a sequence of TestSuites, one more than classes

    Tests of type classes[i] are added to bins[i],
    tests with no match found in classes are place in bins[-1]
    """
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            partition_suite(test, classes, bins)
        else:
            for i in range(len(classes)):
                if isinstance(test, classes[i]):
                    bins[i].addTest(test)
                    break
                else:
                    bins[-1].addTest(test)

