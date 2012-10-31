"""Django test runner which uses behave for BDD tests.
"""

import unittest
from pdb import set_trace
from os.path import dirname, abspath, join, isdir

from django.test.simple import DjangoTestSuiteRunner, reorder_suite
from django.test import LiveServerTestCase
from django.db.models import get_app

import behave
from behave.configuration import Configuration, ConfigError
from behave.runner import Runner
from behave.parser import ParserError
from behave.formatter.ansi_escapes import escapes

import sys

def get_features(app_module):
    app_dir = dirname(app_module.__file__)
    features_dir = abspath(join(app_dir, 'features'))
    if isdir(features_dir):
        return features_dir
    else:
        return None

class DjangoBehaveTestCase(LiveServerTestCase):
    def __init__(self, features_dir):
        unittest.TestCase.__init__(self)
        self.features_dir = features_dir
        # sys.argv kludge
        # need to understand how to do this better
        # temporarily lose all the options etc
        # else behave will complain
        old_argv = sys.argv
        sys.argv = old_argv[:2]
        self.behave_config = Configuration()
        sys.argv = old_argv
        # end of sys.argv kludge
        self.behave_config.paths = [features_dir]
        self.behave_config.format = ['pretty']

        self.behave_config.server_url = 'http://localhost:8081'

        # disable these in case you want to add set_trace in the tests you're developing
        self.behave_config.stdout_capture = False
        self.behave_config.stderr_capture = False

    def runTest(self, result=None):
        # run behave on a single directory
        print "run: features_dir=%s" % (self.features_dir)

        # from behave/__main__.py
        stream = self.behave_config.output
        runner = Runner(self.behave_config)
        try:
            failed = runner.run()
        except ParserError, e:
            sys.exit(str(e))
        except ConfigError, e:
            sys.exit(str(e))

        if self.behave_config.show_snippets and runner.undefined:
            msg = u"\nYou can implement step definitions for undefined steps with "
            msg += u"these snippets:\n\n"
            printed = set()

            if sys.version_info[0] == 3:
                string_prefix = "('"
            else:
                string_prefix = u"(u'"

            for step in set(runner.undefined):
                if step in printed:
                    continue
                printed.add(step)

                msg += u"@" + step.step_type + string_prefix + step.name + u"')\n"
                msg += u"def impl(context):\n"
                msg += u"    assert False\n\n"

            sys.stderr.write(escapes['undefined'] + msg + escapes['reset'])
            sys.stderr.flush()

        self.assertFalse(failed)
        
def make_test_suite(features_dir):
    return DjangoBehaveTestCase(features_dir=features_dir)

class DjangoBehave_Runner(DjangoTestSuiteRunner):
    def build_suite(self, test_labels, extra_tests=None, **kwargs):

        # build standard Django test suite
        #suite = DjangoTestSuiteRunner.build_suite(self, test_labels, extra_tests, **kwargs)

        #
        # TEMP: for now, ignore any tests but feature tests
        # This will become an option
        #
        #suite = unittest.TestSuite()
        suite = super(DjangoBehave_Runner, self).build_suite(test_labels, extra_tests, **kwargs)
        
        #
        # Add any BDD tests to it
        #

        # always get all features for given apps (for convenience)
        for label in test_labels:
            if '.' in label:
                print "Ignoring label with dot in: " % label
                continue
            app = get_app(label)
            
            # Check to see if a separate 'features' module exists,
            # parallel to the models module
            features_dir = get_features(app)
            if features_dir is not None:
                # build a test suite for this directory
                features_test_suite = make_test_suite(features_dir)
                suite.addTest(features_test_suite)

        return reorder_suite(suite, (LiveServerTestCase,))

# eof:
