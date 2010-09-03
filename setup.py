import os
from setuptools import setup, find_packages

setup(
    name='django-constance',
    version='0.1',
    description='Django live settings stored in redis',
    author='Comoga Django Team',
    author_email='comoga@bitbucket.org',
    license='GPL',
    keywords='django libraries settings redis'.split(),
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    test_suite='tests.runtests.runtests',
)

