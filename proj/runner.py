from django_behave.runner import DjangoBehaveTestCase, DjangoBehaveTestSuiteRunner


class ChromeTestCase(DjangoBehaveTestCase):
    def get_browser(self):
        return webdriver.Chrome()


class ChromeRunner(DjangoBehaveTestSuiteRunner):
    def make_bdd_test_suite(self, features_dir):
        return ChromeTestCase(features_dir=features_dir)
