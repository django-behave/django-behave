GOALS:

- To provide a Cucumber-compatible BDD toolset for Django;
- To work well with existing Django testing behaviour e.g. use a test database
- To use Cucumber/Gherkin syntax.
- To provide a library of django-useful steps.

HOW TO USE:

- add 'django_behave' as app
- set TEST_RUNNER to 'django_behave.runner.DjangoBehaveTestSuiteRunner'
- add features directories to apps
- copy django_behave/steps_library.py, if wanted.
