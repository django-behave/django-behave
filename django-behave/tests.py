"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.core.management import call_command

## class CommandText(TestCase):
##     def test_command_exists(self):
## 	call_command('test_bdd')
        
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

## class BDD_TestCase(LiveServerTestCase):

##     @classmethod
##     def setUpClass(cls):
##         cls.selenium = WebDriver()
##         super(BDD_TestCase, cls).setUpClass()

##     @classmethod
##     def tearDownClass(cls):
##         super(BDD_TestCase, cls).tearDownClass()
##         cls.selenium.quit()

# eof
