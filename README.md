# GDAS CMAQ Preprocessor

[![Documentation Status](https://readthedocs.org/projects/gdas-cmaqprep/badge/?version=latest)](https://gdas-cmaqprep.readthedocs.io/en/latest/?badge=latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

A Python tool for processing GDAS (Global Data Assimilation System) data for use with the CMAQ (Community Multiscale Air Quality) modeling system.

## Features

- Downloads GDAS data from NOAA AWS S3 repository
- Processes GDAS grib2 files to extract total column ozone
- Interpolates data to desired grid resolution
- Outputs in CMAQ-compatible formats (NetCDF and ASCII)
- Supports parallel downloads and processing
- Configurable via YAML configuration files

## Installation

### Using Conda (recommended)

This is recommended in order to get grib2io's C dependencies installed.

After activating your Conda environment:

```bash
conda install -c conda-forge grib2io netcdf4 numpy pyyaml requests tqdm xarray
pip install gdas-cmaqprep --no-deps
```

### Using pip

```bash
pip install gdas-cmaqprep
```

### Development Installation

```bash
git clone https://github.com/noaa-oar-arl/gdas-cmaqprep.git
cd gdas-cmaqprep
pip install -e ".[dev]"
```

## Quick Start

1. Create a configuration file (config.yml):

```yaml
start_date: "2024-01-01"
end_date: "2024-01-03"
input_dir: "input"
output_dir: "output"
nlat: 720
nlon: 1440
lat_border: 0.125
use_prev_date: true
gdas:
  hours: [12]
```

2. Run the processor:

```bash
python -m gdas_cmaqprep -c config.yml --download
```

## Usage Examples

### Process from yaml file

```bash
python -m gdas_cmaqprep -c config.yml
```

### Process a Single Date

```bash
python -m gdas_cmaqprep -c config.yml --start-date 2024-01-01
```

### Process a Date Range

```bash
python -m gdas_cmaqprep -c config.yml --start-date 2024-01-01 --end-date 2024-01-31
```

### Download and Process Data

```bash
python -m gdas_cmaqprep -c config.yml --download --max-workers 4
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| start_date | Start date for processing (YYYY-MM-DD) | Required |
| end_date | End date for processing (YYYY-MM-DD) | Required |
| input_dir | Directory containing GDAS files | "input" |
| output_dir | Directory for output files | "output" |
| nlat | Number of latitude points | 720 |
| nlon | Number of longitude points | 1440 |
| lat_border | Latitude border in degrees | 0.125 |
| use_prev_date | Use previous date for missing values | true |

See the [documentation](https://gdas-cmaqprep.readthedocs.io/) for complete configuration options.

## Output Formats

The processor generates two types of output files:

1. **NetCDF Files**: CMAQ-compatible format following IOAPI conventions (optional)
   - Filename pattern: `gdas_cmaq_YYYYMMDD.nc`

2. **ASCII Files**: Traditional CMAQ OMI format
   - Filename pattern: `gdas_cmaq_YYYYMMDD.dat`
   - Optional combined file: `omi_cmaq_combined.dat`

## Documentation

Full documentation is available at [gdas-cmaqprep.readthedocs.io](https://gdas-cmaqprep.readthedocs.io/)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.rst) for details.

## Authors

- NOAA Air Resources Laboratory

## Acknowledgments

- NOAA Global Data Assimilation System (GDAS)
- USEPA Community Multiscale Air Quality (CMAQ) Modeling System

## Disclaimer
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