from behave import *

"""
This file contains some useful generic steps for use with
the splinter web automation library.

http://splinter.cobrateam.info/

The following user roles are used:
'the user': a user without admin privileges
'the adminuser': a user with admin privileges

"""

@given(u'any startpoint')
def any_startpoint(context):
    assert True

@given(u'the user accesses the url "{url}"')
def the_user_accesses_the_url(context, url):
    full_url = ''.join([context.config.server_url, url])
    context.browser.visit(full_url)


def get(context, url_part):
    full_url = get_url(context, url_part)
    return page, resources = context.browser.get(full_url)

def get_url(context, url_part):
    if url_part[0] == '/': url_part = url_part[1:]
    server_url = context.config.server_url if context.config.server_url[-1] == '/' else '%s/' % (context.config.server_url,)
    return '%s%s' % (server_url, url_part,)


@given(u'I am on "{url}"')
def i_am_on(context, url):
    return get(context, url)

@given(u'the user accesses the url "{url}"')
def the_user_accesses_the_url(context, url):
    full_url = ''.join(['http://localhost:8081', url])
    context.browser.visit(full_url)

@then(u'the page contains the h1 "{h1}"')
def the_page_contains_the_h1(context, h1):
    page_h1 = context.browser.find_by_tag('h1').first
    assert h1 == page_h1.text, "Page should contain h1 '%s', has '%s'" % (h1, page_h1.text)

@given(u'a non-logged-in user accesses the url "{url}"')
def a_non_logged_in_user_accesses_the_url(context, url):
    full_url = ''.join(['http://localhost:8081', url])
    context.browser.visit(full_url)

@then(u'the user is shown the page "{url}"')
def the_user_is_shown_the_page(context, url):
    _, short_url = context.browser.url.split('http://localhost:8081')
    assert url == short_url, "Expected url '%s', is instead '%s'" % (url, short_url)

@given(u'the user is shown the login page')
def the_user_is_shown_the_login_page(context):
    return the_user_is_shown_the_page(context, '/accounts/login/')

@then(u'the user is shown the home page')
def the_user_is_shown_the_home_page(context):
    return the_user_is_shown_the_page(context, '/')

@given(u'the user logins as an admin user')
def impl(context):
    assert False

# eof
