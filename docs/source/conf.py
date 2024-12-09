# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EKG Analize'
copyright = '2024, Abdulbosit Tuychiev'
author = 'Abdulbosit Tuychiev'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # Python kodini hujjatlarga kiritish uchun
    'sphinx.ext.napoleon',  # Google va NumPy uslubidagi docstringlarni qo'llab-quvvatlash uchun
]
templates_path = ['_templates']
exclude_patterns = []

language = "['en','ru','uz']"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
