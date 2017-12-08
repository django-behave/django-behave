# coding=utf-8
try:
    import unittest2 as unittest  # import unittest2 for 2.6
except ImportError:
    import unittest

import subprocess
from collections import namedtuple

Std = namedtuple('std', ['out', 'err'])
apps = ['example_app', 'apps.another_example_app']


class BehaveTest(unittest.TestCase):
    def run_test(self, app='example_app', settings='example_proj.settings',
                 management_args=None, **kwargs):
        """
        test the given app with the given management_args and kwargs passed to
        manage.py. kwargs are converted from {'a': 'b'} to --a b

        returns an Std named tuple of strings: (out, err)
        """
        args = [] if management_args is None else list(management_args)
        kwargs['settings'] = settings
        for k, v in kwargs.items():
            args += ['--%s' % k, v]
        p = subprocess.Popen(['./manage.py', 'test', app] + args,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.communicate()
        return Std(*[str(item) for item in out])

    def test_runner_with_default_args_expect_bdd_tests_run(self):
        for app in apps:
            actual = self.run_test(app=app)

            self.assertIn('scenario passed', actual.out)

    def test_runner_with_failfast_and_failing_unittest_expect_bdd_tests_not_run(
            self):
        for app in apps:
            actual = self.run_test(management_args=['--failfast'], app=app)

        self.assertNotIn('scenarios passed', actual.out)

    def test_runner_with_old_tag_specified_expect_only_old_bdd_test_run(self):
        results = ['1 scenario passed, 0 failed, 1 skipped',
                   '0 scenarios passed, 0 failed, 1 skipped']
        for i, app in enumerate(apps):
            actual = self.run_test(app=app, behave_tags='@old')

            self.assertIn(results[i], actual.out)

    def test_runner_with_undefined_steps_expect_display_undefined_steps(self):
        actual = self.run_test()

        self.assertIn(
            'You can implement step definitions for undefined steps with',
            actual.err)


class BehaveOnlyTest(unittest.TestCase):
    def run_test(self, app='example_app', management_args=None,
                 settings='example_proj.bddonly_settings', **kwargs):
        """
        test the given app with the given args and kwargs passed to manage.py.
        kwargs are converted from {'a': 'b'} to --a b

        returns an Std named tuple of strings: (out, err)
        """
        args = [] if management_args is None else list(management_args)
        kwargs['settings'] = settings
        for k, v in kwargs.items():
            args += ['--%s' % k, v]
        p = subprocess.Popen(['./manage.py', 'test', app] + args,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.communicate()
        return Std(*[str(item) for item in out])

    def test_runner_with_default_args_expect_bdd_tests_run(self):
        for app in apps:
            actual = self.run_test(app=app)

            self.assertIn('scenario passed', actual.out)

    def test_runner_with_failfast_and_failing_unittest_expect_bdd_tests_not_run(
            self):
        # When using failfast with BahaveOnlyTestRunner the failing unit test is
        # excluded from the test suite and scenarios get executed.
        # Therefore scenario passed should be found in actual.out
        for app in apps:
            actual = self.run_test(management_args=['--failfast'], app=app)

        self.assertNotIn('scenarios passed', actual.out)


    def test_runner_with_old_tag_specified_expect_only_old_bdd_test_run(self):
        results = ['1 scenario passed, 0 failed, 1 skipped',
                   '0 scenarios passed, 0 failed, 1 skipped']
        for i, app in enumerate(apps):
            actual = self.run_test(app=app, behave_tags='@old')

            self.assertIn(results[i], actual.out)


    def test_runner_with_undefined_steps_expect_display_undefined_steps(self):
        actual = self.run_test()

        self.assertIn('You can implement step definitions for undefined steps with', actual.err)


if __name__ == '__main__':
    unittest.main()
