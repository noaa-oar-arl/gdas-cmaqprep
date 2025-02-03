Configuration
=============

The GDAS CMAQ Preprocessor uses YAML configuration files for setup. Here's a complete reference of all available options.

Basic Configuration
-------------------

.. code-block:: yaml

    # Input/Output
    input_dir: /path/to/input
    output_dir: /path/to/output

    # Grid Settings
    nlat: 180
    nlon: 360
    lat_border: 1.0

    # Processing Options
    use_prev_date: false
    create_full_files: false
    combine_output: true

    # GDAS Settings
    gdas:
      hours: [0, 6, 12, 18]
      base_url: "https://noaa-gfs-bdp-pds.s3.amazonaws.com"
      file_pattern: "gdas.t{hour:02d}z.sfluxgrbf00.grib2"
      local_pattern: "gdas_{date:%Y%m%d}_{hour:02d}.grib2"

Configuration Options
---------------------

Input/Output Settings
~~~~~~~~~~~~~~~~~~~~~

input_dir
    Directory containing GDAS input files

output_dir
    Directory where processed files will be written

Grid Settings
~~~~~~~~~~~~~

nlat
    Number of latitude points in output grid

nlon
    Number of longitude points in output grid

lat_border
    Latitude border in degrees to avoid polar regions

Processing Options
~~~~~~~~~~~~~~~~~~

use_prev_date
    Whether to use previous date's data for missing values

create_full_files
    Create full resolution output files

combine_output
    Combine daily files into a single output file

GDAS Settings
~~~~~~~~~~~~~

hours
    List of hours to process (typically [0, 6, 12, 18])

base_url
    Base URL for NOAA's AWS S3 bucket

file_pattern
    Pattern for remote GDAS files

local_pattern
    Pattern for local GDAS files

Example Configuration
---------------------

.. code-block:: yaml

    # Basic example configuration
    input_dir: ./data/input
    output_dir: ./data/output
    nlat: 180
    nlon: 360
    lat_border: 1.0
    use_prev_date: false
    create_full_files: false
    combine_output: true

    gdas:
      hours: [0, 6, 12, 18]
      base_url: "https://noaa-gfs-bdp-pds.s3.amazonaws.com"
      file_pattern: "gdas.t{hour:02d}z.sfluxgrbf00.grib2"
      local_pattern: "gdas_{date:%Y%m%d}_{hour:02d}.grib2"
