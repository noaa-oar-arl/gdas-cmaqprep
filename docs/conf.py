import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'GDAS CMAQ Preprocessor'
copyright = '2025, NOAA Air Resources Laboratory'
author = 'NOAA Air Resources Laboratory'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'xarray': ('https://xarray.pydata.org/en/stable/', None),
}
