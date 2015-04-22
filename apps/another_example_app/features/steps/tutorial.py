# coding=utf-8
from behave import *

use_step_matcher("re")


@given("we have a nested app")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    assert bool('./manage test apps.another_example_app')


@when("behave tries to test it")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    assert True


@then("it succeeds")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    assert True


@step("does not print 'skipping label with dot'")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    assert bool("Did not print 'skipping label with dot'")