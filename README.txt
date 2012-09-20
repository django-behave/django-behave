GOALS:

- To provide a Cucumber-compatible BDD toolset for Django;
- To work well with existing Django testing behaviour e.g. use a test database
- To use Cucumber/Gherkin syntax.
- To provide a library of django-useful steps.

HOW TO USE:

- add 'django-behave' as app
- set TEST_RUNNER to 'django_behave.runner.DjangoBehave_Runner'
- add features directories to apps
- copy django-behave/features/steps/library.py, if wanted.
