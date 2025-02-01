import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'GDAS CMAQ Preprocessor'
copyright = '2025, NOAA Air Resources Laboratory'
author = 'NOAA Air Resources Laboratory'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    "sphinx_autosummary_accessors",
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    "sphinx.ext.extlinks",
    "sphinx.ext.linkcode",
    'myst_parser'
]

extlinks = {
    "issue": ("https://github.com/noaa-oar-arl/gdas_cmaqprep/issues/%s", "GH"),
    "pull": ("https://github.com/noaa-oar-arl/gdas_cmaqprep/pull/%s", "PR"),
}

autosummary_generate = True  # default in Sphinx v4
autodoc_default_options = {
    "members": True,
    "special-members": "__init__",
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'xarray': ('https://xarray.pydata.org/en/stable/', None),
}
