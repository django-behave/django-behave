from distutils.core import setup


setup(
    name='django-behave',
    packages=['django_behave'],
    version='0.1.1',
    description='Django Test Runner for the Behave BDD module',
    author='Rachel Willmer',
    author_email='rachel@willmer.org',
    url='https://github.com/rwillmer/django-behave',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Testing',
    ],
    install_requires=[
        'Django>=1.4',
        'selenium',
        'parse',
        'behave',
    ]
)
