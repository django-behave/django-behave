"""Django test runner which uses behave for BDD tests.
"""

import unittest
from pdb import set_trace
from os.path import dirname, abspath, join, isdir

from django.test.simple import DjangoTestSuiteRunner, reorder_suite
from django.test.testcases import TestCase
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

class BehaveTestCase(unittest.TestCase):
    def __init__(self, features_dir):
        unittest.TestCase.__init__(self)
        self.features_dir = features_dir
        self.behave_config = Configuration()
        self.behave_config.paths = [features_dir]
        self.behave_config.format = ['pretty']

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

        if failed:
            sys.exit(1)

        
        
def make_test_suite(features_dir):
    return BehaveTestCase(features_dir=features_dir)

class DjangoBehave_Runner(DjangoTestSuiteRunner):
    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        # build standard Django test suite
        suite = DjangoTestSuiteRunner.build_suite(self, test_labels, extra_tests, **kwargs)

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

	return reorder_suite(suite, (TestCase,))

# eof:
