# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
import sys
from datetime import datetime


def get_version():
    with open('../pyproject.toml') as f:
        for line in f:
            match = re.match(r'version = "(.*)"', line)
            if match:
                return match.group(1)
    return '0.0.0'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('extensions'))
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'django-constance'
project_copyright = datetime.now().year.__str__() + ', Jazzband'

# The full version, including alpha/beta/rc tags
release = get_version()
# The short X.Y version
version = '.'.join(release.split('.')[:3])

# -- General configuration ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_search.extension',
    'settings',
]

templates_path = ['_templates']
source_suffix = '.rst'
root_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
html_last_updated_fmt = ''

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'django-constancedoc'

# -- Options for LaTeX output ---------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-latex-output

latex_elements = {}

latex_documents = [
    ('index', 'django-constance.tex', 'django-constance Documentation', 'Jazzband', 'manual'),
]

# -- Options for manual page output ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-manual-page-output

man_pages = [('index', 'django-constance', 'django-constance Documentation', ['Jazzband'], 1)]

# -- Options for Texinfo output -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-texinfo-output

texinfo_documents = [
    (
        'index',
        'django-constance',
        'django-constance Documentation',
        'Jazzband',
        'django-constance',
        'One line description of project.',
        'Miscellaneous',
    ),
]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'django': ('https://docs.djangoproject.com/en/dev/', 'https://docs.djangoproject.com/en/dev/_objects/'),
}
