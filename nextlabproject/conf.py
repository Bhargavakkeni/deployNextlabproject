# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0,os.path.abspath('C:/Users/ganes/OneDrive/Desktop/NextLabs/webapp/nextlabproject'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.nextlabproject.nextlabproject.settings'
project = 'nextlabproject'
copyright = '2023, Bhargav'
author = 'Bhargav'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

autodoc_mock_imports = [
    "rest_framework",
    "django",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
