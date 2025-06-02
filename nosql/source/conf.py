# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0,os.path.abspath('..'))

#sys.path += ['..','../nosql/']
#sys.path.append('../nosql/')

#sys.path.append(os.path.abspath('../nosql/'))


             
project = 'MLOPS'
copyright = '2025, Jan Jansen'
author = 'Jan Jansen'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_markdown_builder',
    'sphinx.ext.autodoc',
    'sphinxcontrib.blockdiag',
]

blockdiag_html_image_format = 'PNG'  # LaTeX typically works better with PNG
blockdiag_latex_image_format = 'PNG'  # Explicitly set the LaTeX format

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
