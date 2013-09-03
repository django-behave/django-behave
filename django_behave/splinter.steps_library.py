from urlparse import urljoin

from behave import *

"""
This file contains some useful generic steps for use with
the splinter web automation library.

http://splinter.cobrateam.info/

The following user roles are used:
'the user': a user without admin privileges
'the adminuser': a user with admin privileges

This is a Work-In-Progress
"""


@given(u'any startpoint')
def any_startpoint(context):
    assert True


@given(u'the user accesses the url "{url}"')
def the_user_accesses_the_url(context, url):
    full_url = urljoin(context.config.server_url, url)
    context.browser.visit(full_url)


@then(u'the url is "{url}"')
def the_url_is(context, url):
    path_info = context.browser.url.replace(context.config.server_url, '')
    assert path_info == url


@then(u'the page contains the h1 "{h1}"')
def the_page_contains_the_h1(context, h1):
    page_h1 = context.browser.find_by_tag('h1').first
    assert h1 == page_h1.text, "Page should contain h1 '%s', has '%s'" % (h1, page_h1.text)


# TODO
# @given(u'a non-logged-in user accesses the url "{url}"')
# def a_non_logged_in_user_accesses_the_url(context, url):
#     full_url = ''.join(['http://localhost:8081', url])
#     context.browser.visit(full_url)


@given(u'the user is shown the login page')
def the_user_is_shown_the_login_page(context):
    return the_url_is(context, '/accounts/login/')


@then(u'the user is shown the home page')
def the_user_is_shown_the_home_page(context):
    return the_url_is(context, '/')


# TODO
# @given(u'the user logins as an admin user')
# def impl(context):
#     assert False

# eof
