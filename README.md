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

- add 'django_behave' as app
- set TEST_RUNNER to 'django_behave.runner.DjangoBehave_Runner'
- add features directories to apps
- copy django_behave/features/steps/library.py, if wanted.

REQUIREMENTS
============

The main one is the 'behave' module, of course, which provides the BDD toolset for Python.

Also used are:
- django >= 1.4 (needed for the LiveServerTestCase)
- selenium
- splinter

See requirements.txt for details.

