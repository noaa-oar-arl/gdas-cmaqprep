GDAS CMAQ Preprocessor Documentation
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   configuration
   api
   contributing
   license
   modules

Overview
--------

The GDAS CMAQ Preprocessor is a tool for processing GDAS (Global Data Assimilation System) data for use with the CMAQ (Community Multiscale Air Quality) modeling system.

Features
--------

* Downloads GDAS data from NOAA AWS S3 repository
* Processes GDAS grib2 files to extract total column ozone
* Interpolates data to desired grid resolution
* Outputs in CMAQ-compatible formats (NetCDF and ASCII)
* Supports parallel downloads and processing
* Configurable via YAML configuration files

Quick Start
-----------

1. Install the package::

    pip install gdas-cmaqprep

2. Create a configuration file (config.yml)
3. Run the processor::

    python src/create_gdas_cmaq_input.py --config config.yml

For more detailed information, please see the :doc:`usage` and :doc:`configuration` pages.

License
-------

.. include:: ../../LICENSE
   :literal:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
