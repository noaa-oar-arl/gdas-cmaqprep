GDAS CMAQ Preprocessor Documentation
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   installation
   usage
   configuration
   api
   contributing
   license

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

Disclaimer
----------

The United States Department of Commerce (DOC) GitHub project code is
provided on an 'as is' basis and the user assumes responsibility for
its use.  DOC has relinquished control of the information and no
longer has responsibility to protect the integrity, confidentiality,
or availability of the information.  Any claims against the Department
of Commerce stemming from the use of its GitHub project will be
governed by all applicable Federal law.  Any reference to specific
commercial products, processes, or services by service mark,
trademark, manufacturer, or otherwise, does not constitute or imply
their endorsement, recommendation or favoring by the Department of
Commerce.  The Department of Commerce seal and logo, or the seal and
logo of a DOC bureau, shall not be used in any manner to imply
endorsement of any commercial product or activity by DOC or the United
States Government.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
