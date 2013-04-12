import os
from setuptools import setup, find_packages

# work around to prevent http://bugs.python.org/issue15881 from showing up
try:
    import multiprocessing
except ImportError:
    pass

try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
    long_description = f.read().strip()
    f.close()
except IOError:
    long_description = None

setup(
    name='django-constance',
    version='0.6',
    url="http://github.com/comoga/django-constance",
    description='Django live settings with pluggable backends, including Redis.',
    long_description=long_description,
    author='Comoga Django Team',
    author_email='dev@comoga.cz',
    maintainer='Jannis Leidel',
    maintainer_email='jannis@leidel.info',
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    test_suite='tests.runtests.main',
    tests_require=['django-discover-runner', 'django-picklefield', 'redis'],
    install_requires=['six'],
    extras_require={
        'database':  ['django-picklefield'],
        'redis': ['redis'],
    }
)
