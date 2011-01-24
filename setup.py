import os
from setuptools import setup, find_packages


try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
    long_description = f.read().strip()
    f.close()
except IOError:
    long_description = None

setup(
    name='django-constance',
    version='0.2',
    url="http://github.com/comoga/django-constance",
    description='Django live settings stored in redis',
    long_description=long_description,
    author='Comoga Django Team',
    author_email='dev@comoga.cz',
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

