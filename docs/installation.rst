Installation
===========

Requirements
-----------

Core Requirements:
~~~~~~~~~~~~~~~~

* Python 3.8 or later
* grib2io
* xarray
* netCDF4
* numpy
* pyyaml
* requests

Optional Requirements:
~~~~~~~~~~~~~~~~~~

* tqdm (for progress bars)

Basic Installation
----------------

You can install the package using pip::

    pip install gdas-cmaqprep

With progress bar support::

    pip install "gdas-cmaqprep[progress]"

Development Installation
----------------------

For development installation::

    git clone https://github.com/noaa-arl/gdas_cmaqprep.git
    cd gdas_cmaqprep
    pip install -e ".[dev,progress]"
