from django.test import TestCase

# Create your tests here.

class ExampleTest(TestCase):
    def test_failing(self):
        """ This is a failing unit test """
        self.assertTrue(False)

    def test_passing(self):
        """ This is a passing unit test """
        self.assertTrue(True)
