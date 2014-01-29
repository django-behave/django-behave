import unittest
import subprocess

class BehaveTest(unittest.TestCase):
    def run_test(self, app='example_app', settings='example_proj.settings', *args, **kwargs):
        """
        test the given app with thiegiven args and kwargs passed to manage.py. kwargs are converted from
        {'a': 'b'} to --a=b

        returns a tuple: (stdout, stderr)
        """
        kwargs['settings'] = settings
        kwargs = ['--{}={}'.format(k, v) for k, v in kwargs.items()]
        p = subprocess.Popen(['./manage.py', 'test', app] + list(args) + kwargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.communicate()

    def test_runner_with_default_args_expect_bdd_tests_run(self):
        actual = self.run_test()

        self.assertIn('scenario passed', actual[0])

    def test_runner_with_failfast_and_failing_unittest_expect_bdd_tests_not_run(self):
        actual = self.run_test('--failfast')

        self.assertNotIn('scenario passed', actual[0])

    def test_runner_with_old_tag_specified_expect_only_old_bdd_test_run(self):
        actual = self.run_test('--behave_tags @old')

        self.assertIn('1 scenario passed, 0 failed, 1 skipped', actual[0])

if __name__ == '__main__':
    unittest.main()

"""

import subprocess
p = subprocess.Popen(['./manage.py', 'test', 'example_app', '--failfast', '--settings=example_proj.settings'], stdout=subprocess.PIPE)
out = p.communicate()[0]

import sys
from cStringIO import StringIO
def test():
    backup_out = sys.stdout
    sys.stdout = StringIO()
    backup_err = sys.stderr
    sys.stderr = StringIO()
    try:
        from django.core.management import call_command
        call_command('test', 'example_app')
    except SystemExit:
        print 'attempted exit!'
    out = sys.stdout.getvalue()
    err = sys.stderr.getvalue()
    sys.stdout.close()
    sys.stderr.close()
    sys.stdout = backup_out
    sys.stderr = backup_err
    return out, err
"""