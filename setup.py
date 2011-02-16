from setuptools import setup, find_packages
from setuptools.command.test import test

class TestRunner(test):
    def run(self, *args, **kwargs):
        from runtests import runtests
        runtests()

setup(
    name='djanginxed',
    version='0.0.5',
    description='Django Nginx Memcached integration.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/shaunsephton/djanginxed',
    packages = find_packages(),
    include_package_data=True,
    install_requires=[
        'django-snippetscream',
    ],
    test_suite = 'djanginxed.tests',
    cmdclass={"test": TestRunner},
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
