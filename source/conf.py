# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = 'Br6.in'
copyright = '2024, Ege Dogan Dursun'
author = 'Ege Dogan Dursun'
release = 'v0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    # 'sphinx.ext.viewcode',  # Comment this out or remove it
]

autosummary_generate = True  # Automatically generate summary tables

templates_path = ['_templates']
exclude_patterns = []

# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath('../'))  # Adjust the number of '../' based on where your conf.py is located
sys.path.insert(0, os.path.abspath('../apps/'))  # Path to the 'apps' directory

# Ensure your Django settings are configured before Sphinx attempts to import any Django modules
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django

django.setup()

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
