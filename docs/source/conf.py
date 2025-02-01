import os
import sys

# Add the project root directory and src directory to the Python path
sys.path.insert(0, os.path.abspath('../..'))

# Configuration for autodoc
autodoc_mock_imports = [
    'numpy',
    'xarray',
    'netCDF4',
    'yaml',
    'requests',
    'tqdm'
]

# Add both project root and src directory to Python path
sys.path.insert(0, os.path.abspath('../../src'))

project = 'GDAS CMAQ Preprocessor'
copyright = '2024'
author = 'Author'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add any files you want to copy from the root to the docs
html_extra_path = ['../../LICENSE']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'xarray': ('https://docs.xarray.dev/en/stable/', None),
}
