project = 'GDAS CMAQ Preprocessor'
copyright = '2025, NOAA Air Resources Laboratory'
author = 'NOAA Air Resources Laboratory'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    "sphinx.ext.extlinks",
    # "sphinx.ext.linkcode",
    'myst_parser'
]

extlinks = {
    "issue": ("https://github.com/noaa-oar-arl/gdas-cmaqprep/issues/%s", "GH"),
    "pull": ("https://github.com/noaa-oar-arl/gdas-cmaqprep/pull/%s", "PR"),
}

autosummary_generate = True  # default in Sphinx v4
autodoc_default_options = {
    "members": True,
    "special-members": "__init__",
}
# Configuration for autodoc
autodoc_mock_imports = [
    'numpy',
    'xarray',
    # 'netCDF4',
    # 'yaml',
    'requests',
    # 'tqdm'
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
# html_static_path = ['_static']

# Add any files you want to copy from the root to the docs
html_extra_path = ['../../LICENSE']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'xarray': ('https://docs.xarray.dev/en/stable/', None),
}
