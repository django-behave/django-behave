from django.test import TestCase

# Create your tests here.

class ExampleTest(TestCase):
    def test_failing(self):
    	""" This is a failing test """
        self.assertTrue(False)

    def test_passing(self):
        self.assertTrue(True)
