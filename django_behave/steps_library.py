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
