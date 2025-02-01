Installation
============

Requirements
------------

Core Requirements:
~~~~~~~~~~~~~~~~~~

* Python 3.8+
* numpy
* grib2io
* xarray
* netCDF4
* pyyaml
* requests

Optional Requirements:
~~~~~~~~~~~~~~~~~~~~~~

* tqdm (for progress bars)

Basic Installation
------------------

To install the package:

.. code-block:: bash

    pip install -r requirements.txt

Development Installation
------------------------

For development:

.. code-block:: bash

    git clone https://github.com/username/gdas_cmaqprep.git
    cd gdas_cmaqprep
    pip install -e .[dev]
