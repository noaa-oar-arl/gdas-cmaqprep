Usage
=====

Basic Usage
-----------

The basic usage pattern is::

    gdas-cmaqprep --config config.yml --start-date YYYY-MM-DD --end-date YYYY-MM-DD

Command Line Options
--------------------

--config CONFIG, -c CONFIG
    Path to YAML configuration file (default: config.yml)

--start-date START_DATE
    Start date for processing (YYYY-MM-DD format)

--end-date END_DATE
    End date for processing (YYYY-MM-DD format)

--input-dir INPUT_DIR, -i INPUT_DIR
    Input directory containing GDAS files

--output-dir OUTPUT_DIR, -o OUTPUT_DIR
    Output directory for processed files

--download
    Download GDAS data before processing

Additional Options
------------------

--nlat NLAT
    Number of latitude points

--nlon NLON
    Number of longitude points

--lat-border LAT_BORDER
    Latitude border in degrees

--use-prev-date
    Use previous date for missing values

--create-full-files
    Create full resolution output files

--verbose, -v
    Enable verbose logging

Examples
--------

1. Process a single day::

    gdas-cmaqprep -c config.yml --start-date 2024-01-01

2. Process a date range with downloads::

    gdas-cmaqprep -c config.yml --start-date 2024-01-01 --end-date 2024-01-31 --download

3. Override grid resolution::

    gdas-cmaqprep -c config.yml --start-date 2024-01-01 --nlat 180 --nlon 360
