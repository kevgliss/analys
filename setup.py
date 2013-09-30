""" Setup file.
"""
import os
import sys
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(name='Analys',
    version=0.1,
    description='Analys',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
    keywords="web services",
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    #scripts=['/bin/analys'],
    install_requires=['cornice',
					  'PasteScript',
					  'waitress',
					  'pymongo',
					  'redis',
					  'rq',
					  'rarfile',
					  'python-magic',
					  'requests',
					  'docopt'],
                      #'supervisor'],
    entry_points = """\
    [paste.app_factory]
    main = analys:main
    """,
    paster_plugins=['pyramid'],
)
