==================================
=
= LOOKING FOR A NEW MAINTAINER
=
==================================

CAN YOU HELP? 
I don't have the time to maintain this properly. 
Would you like to volunteer to take it over?
Or suggest someone who'd be good to do it?

Thanks
Rachel


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
- decide which automation library you want to use
- setup your environment.py to use this library to open browser (see below)
- copy django_behave/features/steps/library.py, if wanted.

EXAMPLE
=======

Assuming you have a app called proj.apps.myapp

Edit INSTALLED_APPS, as above.
Edit TEST_RUNNER, as above.

Create proj/apps/myapp/features and proj/apps/myapp/features/steps.

Copy example/tutorial.feature to the features dir.
Copy example/tutorial.py to the features/steps dir.

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

AUTOMATION LIBRARY
==================

Django_behave is agnostic about which automation library you use inside the tests.

I like splinter (http://splinter.cobrateam.info).

You will need to setup a browser for use with this library.

For example, my features/environment.py file has this:

    from splinter.browser import Browser

    def before_all(context):
        context.browser = Browser()

    def after_all(context):
        context.browser.quit()
        context.browser = None

COMMAND LINE OPTIONS
====================

It is possible to use Behave command line options.  In order to avoid conflict
with Django's manage.py test options, all options meant for django-behave start
with '--behave_'.  For example, given the following Behave command:

    behave --no-color --tags @mytag ...
    
this would become:

    ./manage.py test --behave_no-color --behave_tags @mytag ...
    
In addition, the option '--behave_browser' can allow the user to specify which
browser to use for testing.  For example:

    ./manage.py test --behave_browser firefox ...

The splinter before_all() example above could then use this option:

    def before_all(context):
        context.browser = Browser(context.config.browser)

            
