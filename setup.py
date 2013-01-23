import os
from setuptools import setup, find_packages


try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
    long_description = f.read().strip()
    f.close()
except IOError:
    long_description = None

setup(
    name='django-constance-trbs',
    version='0.5.1',
    url="http://github.com/trbs/django-constance-trbs",
    description='Django live settings with pluggable backends, including Redis.',
    long_description=long_description,
    author='Forked from Comoga Django Team',
    author_email='trbs@trbs.net',
    license='BSD',
    keywords='django libraries settings redis'.split(),
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    test_suite='tests.runtests.main',
)

