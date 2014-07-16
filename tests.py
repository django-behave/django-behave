try:
    import unittest2 as unittest  # import unittest2 for 2.6
except ImportError:
    import unittest

import subprocess
from collections import namedtuple

Std = namedtuple('std', ['out', 'err'])

class BehaveTest(unittest.TestCase):
    def run_test(self, app='example_app', settings='example_proj.settings', *args, **kwargs):
        """
        test the given app with the given args and kwargs passed to manage.py. kwargs are converted from
        {'a': 'b'} to --a b

        returns an Std named tuple of strings: (out, err)
        """
        args = list(args)
        kwargs['settings'] = settings
        for k, v in kwargs.items():
            args += ['--%s' % k, v]
        p = subprocess.Popen(['./manage.py', 'test', app] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.communicate()
        return Std(*[str(item) for item in out])

    def test_runner_with_default_args_expect_bdd_tests_run(self):
        actual = self.run_test()

        self.assertIn('scenario passed', actual.out)

    def test_runner_with_failfast_and_failing_unittest_expect_bdd_tests_not_run(self):
        actual = self.run_test('--failfast')

        self.assertNotIn('scenario passed', actual.out)

    def test_runner_with_old_tag_specified_expect_only_old_bdd_test_run(self):
        actual = self.run_test(behave_tags='@old')

        self.assertIn('1 scenario passed, 0 failed, 1 skipped', actual.out)

    def test_runner_with_undefined_steps_expect_display_undefined_steps(self):
        actual = self.run_test()

        self.assertIn('You can implement step definitions for undefined steps with', actual.err)

if __name__ == '__main__':
    unittest.main()
