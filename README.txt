django-behave
=============

A Django TestRunner for the Behave BDD module

GOALS
=====

- To provide a Cucumber-compatible BDD toolset for Django;
- To work well with existing Django testing behaviour e.g. use a test database
- To use Cucumber/Gherkin syntax.
- To provide a library of django-useful steps.

HOW TO USE
==========

- add 'django_behave' to INSTALLED_APPS
- set TEST_RUNNER to 'django_behave.runner.DjangoBehaveTestSuiteRunner'
- add features directories to apps
- copy django_behave/features/steps/library.py, if wanted.

EXAMPLE
=======

Assuming you have a app called proj.apps.myapp

Edit INSTALLED_APPS, as above.
Edit TEST_RUNNER, as above.

Create proj/apps/myapp/fixtures and proj/apps/myapp/fixtures/steps.

Copy example/tutorial.feature to the fixtures dir.
Copy example/tutorial.py to the fixtures/steps dir.

$ python manage.py test myapp

should then show you django-behave in action, finding the tutorial feature
and running the tests.

REQUIREMENTS
============

The main one is the 'behave' module, of course, which provides the BDD toolset for Python.

Also used are:
- django >= 1.4 (needed for the LiveServerTestCase)
- selenium

See requirements.txt for details.

