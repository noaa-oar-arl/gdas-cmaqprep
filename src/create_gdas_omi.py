import argparse
import logging
import traceback
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
import requests
import xarray as xr
import yaml
from netCDF4 import Dataset
import concurrent.futures

# Make tqdm optional
try:
    from tqdm import tqdm
    has_tqdm = True
except ImportError:
    has_tqdm = False
    def tqdm(iterable, **kwargs):
        total = kwargs.get('total', '?')
        desc = kwargs.get('desc', '')
        logger.info(f"{desc} - Starting process with {total} items")
        return iterable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments for GDAS data processing.

    Returns:
        argparse.Namespace: Parsed command line arguments with the following fields:
            - config (str): Path to YAML configuration file
            - start_date (str): Start date in YYYY-MM-DD format
            - end_date (str): End date in YYYY-MM-DD format
            - input_dir (str): Input directory for GDAS files
            - output_dir (str): Output directory for processed files
            - nlat (int): Number of latitude points
            - nlon (int): Number of longitude points
            - lat_border (float): Latitude border in degrees
            - use_prev_date (bool): Whether to use previous date for missing values
            - create_full_files (bool): Whether to create full resolution output files
            - verbose (bool): Enable verbose logging
            - download (bool): Whether to download GDAS data
            - max_workers (int): Maximum number of parallel downloads
    """
    parser = argparse.ArgumentParser(
        description='Process GDAS data for CMAQ model',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-c', '--config',
                      default='config.yml',
                      help='Path to YAML configuration file')

    # Simplify date arguments to just start/end
    parser.add_argument('--start-date',
                      help='Start date for processing (YYYY-MM-DD)')
    parser.add_argument('--end-date',
                      help='End date for processing (YYYY-MM-DD)')

    # Remove redundant date arguments
    #parser.add_argument('-d', '--date', help='Single processing date (YYYY-MM-DD)')
    #parser.add_argument('--date-range', action='store_true', help='Process a date range')

    parser.add_argument('-i', '--input-dir',
                      help='Input directory containing GDAS files (overrides config file)')

    parser.add_argument('-o', '--output-dir',
                      help='Output directory for processed files (overrides config file)')

    parser.add_argument('--nlat',
                      type=int,
                      help='Number of latitude points (overrides config file)')

    parser.add_argument('--nlon',
                      type=int,
                      help='Number of longitude points (overrides config file)')

    parser.add_argument('--lat-border',
                      type=float,
                      help='Latitude border in degrees (overrides config file)')

    parser.add_argument('--use-prev-date',
                      action='store_true',
                      help='Use previous date for missing values (overrides config file)')

    parser.add_argument('--create-full-files',
                      action='store_true',
                      help='Create full resolution output files (overrides config file)')

    parser.add_argument('-v', '--verbose',
                      action='store_true',
                      help='Enable verbose logging')

    parser.add_argument('--download', action='store_true',
                      help='Download GDAS data before processing')
    parser.add_argument('--max-workers',
                      type=int,
                      default=4,
                      help='Maximum number of parallel downloads')

    return parser.parse_args()

def load_config(args):
    """
    :no-index:

    Load and merge configuration from YAML file and command line arguments.

    Handles date parsing, validation, and command line overrides of config values.

    Args:
        args (argparse.Namespace): Parsed command line arguments

    Returns:
        dict: Merged configuration dictionary with validated settings

    Raises:
        ValueError: If required date parameters are missing
        yaml.YAMLError: If YAML config file is invalid
    """
    # Load YAML config
    with open(args.config) as f:
        config = yaml.safe_load(f)

    # Validate and set dates
    if args.start_date:
        config['start_date'] = args.start_date
    if args.end_date:
        config['end_date'] = args.end_date
    elif args.start_date:
        config['end_date'] = args.start_date

    # Ensure dates are present and valid
    if 'start_date' not in config or 'end_date' not in config:
        raise ValueError("Start and end dates must be specified in config file or command line")

    # Convert date strings to datetime
    config['start_date'] = datetime.strptime(config['start_date'], '%Y-%m-%d')
    config['end_date'] = datetime.strptime(config['end_date'], '%Y-%m-%d')

    # Set initial date for first processing
    config['date'] = config['start_date']

    # Override with command line arguments if provided
    for key, value in vars(args).items():
        if value is not None and key in config:
            config[key] = value
            logger.info(f"Overriding {key} from command line: {value}")

    return config

class GDASProcessor:
    """
    :no-index:

    Process GDAS grib2 data files for CMAQ model integration.

    This class handles reading GDAS grib2 files, extracting total column ozone data,
    interpolating to a specified grid, and writing output in both CMAQ-ready netCDF
    and ASCII formats.

    Attributes:
        config (dict): Configuration dictionary containing processing parameters
        lats (numpy.ndarray): Latitude points for output grid
        lons (numpy.ndarray): Longitude points for output grid
        coords (dict): Coordinate dictionary for interpolation
    """

    @staticmethod
    def wrap_longitudes(lons):
        """
        :no-index:

        Convert longitudes from [0, 360) format to [-180, 180) format.

        Args:
            lons (numpy.ndarray): Array of longitude values

        Returns:
            numpy.ndarray: Converted longitude values

        Example:
            >>> GDASProcessor.wrap_longitudes(np.array([350, 10]))
            array([-10, 10])
        """
        return (lons + 180) % 360 - 180

    def __init__(self, config: Dict):
        self.config = config
        self.validate_config()
        outdir = Path(self.config['output_dir'])
        outdir.mkdir(parents=True, exist_ok=True)
        self.setup_grid()

    def validate_config(self):
        """
        :no-index:

        Validate configuration parameters
        """
        required = ['input_dir', 'output_dir', 'date', 'nlat', 'nlon',
                   'lat_border', 'use_prev_date', 'create_full_files']
        missing = [key for key in required if key not in self.config]
        if missing:
            raise ValueError(f"Missing required config parameters: {missing}")

    def setup_grid(self):
        """
        :no-index:

        Setup the lat/lon grid coordinates
        """
        lat_step = (180.0 - 2*self.config['lat_border']) / (self.config['nlat'] - 1)
        self.lats = np.linspace(-90.0 + self.config['lat_border'],
                              90.0 - self.config['lat_border'],
                              self.config['nlat'])
        self.lons = np.linspace(-180.0, 180.0, self.config['nlon'])

        # Create coordinate dictionary for interpolation
        self.coords = {
            'latitude': self.lats,
            'longitude': self.lons
        }

    def read_gdas_file(self, filename: str) -> xr.Dataset:
        """
        :no-index:

        Read and process a GDAS grib2 file to extract total column ozone.

        Args:
            filename (str): Path to GDAS grib2 file

        Returns:
            xarray.Dataset: Dataset containing interpolated total column ozone data

        Raises:
            Exception: If file reading or processing fails

        Notes:
            - Uses grib2io backend for efficient reading
            - Automatically handles longitude wrapping and grid interpolation
            - Returns data interpolated to the configured output grid
        """
        try:
            # Use xarray with grib2io backend and filter for total ozone
            filters = dict(typeOfFirstFixedSurface=200)  # Filter for column ozone
            ds = xr.open_dataset(filename, engine='grib2io', filters=filters)['TOZNE']

            # Get coordinates and wrap longitudes to [-180, 180]
            lons = self.wrap_longitudes(ds.longitude.values[0,:])
            ds['x'] = lons
            ds['y'] = ds.latitude.values[:,0]

            logger.debug(f"Longitude range: {ds.x.min().item():.1f} to {ds.x.max().item():.1f}")

            # Interpolate to desired grid
            return ds.interp(
                y=self.coords['latitude'],
                x=self.coords['longitude']
            )

        except Exception as e:
            logger.error(f"Error reading file {filename}: {e}")
            logger.debug(traceback.format_exc())
            raise

    def fill_missing_values(self, ds: xr.Dataset) -> xr.Dataset:
        """
        :no-index:

        Fill missing values in Dataset

        Args:
            ds: Dataset containing data to fill

        Returns:
            Dataset with filled values
        """
        if not self.config['use_prev_date']:
            return ds

        # Fill missing values using interpolation
        ds = ds.interpolate_na(dim='lon', method='nearest')
        ds = ds.interpolate_na(dim='lat', method='nearest')

        return ds

    def write_cmaq_format(self, date: date, data: np.ndarray):
        """
        :no-index:

        Write data in CMAQ-compatible netCDF format following IOAPI conventions.

        Creates a CMAQ-ready netCDF file with proper IOAPI attributes and variables.

        Args:
            date (datetime.date): Date of the data
            data (numpy.ndarray): 2D array of ozone column data

        Notes:
            - Creates IOAPI-compliant netCDF files
            - Sets required global attributes and dimensions
            - Includes proper time flags and variable metadata
            - Output filename format: gdas_cmaq_YYYYMMDD.nc
        """
        outfile = Path(self.config['output_dir']) / f"gdas_cmaq_{date:%Y%m%d}.nc"

        # Calculate IOAPI date format (YYYYDDD)
        ioapi_date = int(date.strftime('%Y') + str(date.timetuple().tm_yday).zfill(3))

        with Dataset(outfile, 'w', format='NETCDF4') as nc:
            # IOAPI Required Global Attributes
            nc.IOAPI_VERSION = "$Id: @(#) ioapi library version 3.2 $"
            nc.EXEC_ID = "????????????????"
            nc.FTYPE = 1  # GRDDED3
            nc.CDATE = int(datetime.now().strftime('%Y%j'))
            nc.CTIME = int(datetime.now().strftime('%H%M%S'))
            nc.WDATE = nc.CDATE
            nc.WTIME = nc.CTIME
            nc.SDATE = ioapi_date
            nc.STIME = 0
            nc.TSTEP = 240000  # Daily file (24 hours * 10000)
            nc.NTHIK = 1
            nc.NCOLS = len(self.lons)
            nc.NROWS = len(self.lats)
            nc.NLAYS = 1
            nc.NVARS = 1
            nc.GDTYP = 1  # lat-lon
            nc.P_ALP = 0.0
            nc.P_BET = 0.0
            nc.P_GAM = 0.0
            nc.XCENT = 0.0
            nc.YCENT = 0.0
            nc.XORIG = -180.0
            nc.YORIG = float(self.lats[-1])  # Southernmost latitude
            nc.XCELL = 360.0 / len(self.lons)
            nc.YCELL = abs(self.lats[0] - self.lats[-1]) / (len(self.lats) - 1)
            nc.VGTYP = 7  # VGSGPH3: Sigma-P hybrid
            nc.VGTOP = 5000.0
            nc.VGLVLS = [1.0, 0.9975]  # Same as original code
            nc.GDNAM = "OMI_CMAQ"

            # Create dimensions following IOAPI conventions
            nc.createDimension('TSTEP', None)
            nc.createDimension('LAY', nc.NLAYS)
            nc.createDimension('ROW', nc.NROWS)
            nc.createDimension('COL', nc.NCOLS)
            nc.createDimension('VAR', nc.NVARS)
            nc.createDimension('DATE-TIME', 2)

            # Create IOAPI required variables
            tflag = nc.createVariable('TFLAG', 'i4', ('TSTEP', 'VAR', 'DATE-TIME'))
            tflag.units = '<YYYYDDD,HHMMSS>'
            tflag.long_name = 'TFLAG'
            tflag[0, :, 0] = ioapi_date
            tflag[0, :, 1] = 0

            # Create ozone variable
            ozone = nc.createVariable('OZONE_COLUMN', 'f4', ('TSTEP', 'LAY', 'ROW', 'COL'))
            ozone.long_name = 'Total Column Ozone'
            ozone.units = 'DU'
            ozone.var_desc = 'OMI Ozone Column Density'

            # Write data
            ozone[0, 0, :, :] = data

            # Add file description
            nc.FILEDESC = 'CMAQ subset of OMI Satellite Observations'

    def write_dat_format(self, date: date, data: np.ndarray):
        """
        :no-index:

        Write ASCII .dat format output files following CMAQ OMI format
        """
        outfile = Path(self.config['output_dir']) / f"gdas_cmaq_{date:%Y%m%d}.dat"

        year_frac = date.year + (date.timetuple().tm_yday - 1) / 365.0

        # Write header
        with open(outfile, 'w') as f:
            f.write(f"nlat      {len(self.lats)}\n")
            f.write(f"nlon      {len(self.lons)}\n")

            # Write column headers
            f.write("yeardate latitude ")
            for lon in self.lons:
                f.write(f"{lon:7.2f}")
            f.write("\n")

            # Write data rows from north to south
            for i in range(len(self.lats)-1, -1, -1):  # North to South
                lat = self.lats[i]
                f.write(f"{year_frac:9.4f} {lat:7.1f} ")

                # Write ozone values, handling missing values
                for j in range(len(self.lons)):
                    if np.isnan(data[i, j]) or data[i, j] < 0:
                        f.write("     *")  # Missing value indicator
                    else:
                        value = int(round(data[i, j]))
                        f.write(f"{value:6d}")
                f.write("\n")

        logger.info(f"Successfully wrote ASCII file: {outfile}")

    def process_files(self):
        """
        :no-index:

        Process GDAS data files for a single day
        """
        date = self.config['date']
        input_dir = Path(self.config['input_dir'])

        files = []
        pattern = self.config['gdas'].get('local_pattern', "gdas_{date:%Y%m%d}_{hour:02d}.grib2")

        for hour in self.config['gdas']['hours']:
            filename = pattern.format(date=date, hour=hour)
            file_path = input_dir / filename
            if file_path.exists():
                files.append(file_path)

        if not files:
            raise FileNotFoundError(
                f"No GDAS files found for date {date:%Y-%m-%d} using pattern {pattern}"
            )

        logger.info(f"Processing {len(files)} files for {date:%Y-%m-%d}")

        # Process all hours and average them
        datasets = []
        for file in files:
            logger.info(f"Processing {file}")
            ds = self.read_gdas_file(file)
            datasets.append(ds)

        # Average all hours for the day
        daily_ds = xr.concat(datasets, dim='time').mean(dim='time')

        date = self.config['date'].date()
        data = daily_ds.values  # Get numpy array of data values

        logger.info(f"Writing netCDF file for {date}")
        self.write_cmaq_format(date, data)

        logger.info(f"Writing ASCII .dat file for {date}")
        self.write_dat_format(date, data)

    def _get_date_from_filename(self, filename: Path) -> datetime.date:
        """Extract date from filename"""
        # Extract date from gdas_YYYYMMDD_HH.grib2 format
        date_str = filename.stem.split('_')[1]
        return datetime.strptime(date_str, '%Y%m%d').date()

    def _download_single_file(self, date: datetime, hour: int, outdir: Path) -> Optional[Path]:
        """Download a single GDAS file"""
        file_pattern = self.config['gdas']['file_pattern']
        filename = file_pattern.format(hour=hour)
        outfile = outdir / f"gdas_{date:%Y%m%d}_{hour:02d}.grib2"

        # Skip if file already exists
        if outfile.exists():
            logger.debug(f"File already exists: {outfile}")
            return outfile

        # Construct URL using AWS S3 pattern
        url = (f"{self.config['gdas']['base_url']}/gfs.{date:%Y%m%d}/"
               f"{hour:02d}/atmos/{filename}")

        logger.info(f"Downloading {url}")

        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()

            # Save file
            outfile.write_bytes(response.content)
            logger.info(f"Successfully downloaded to {outfile}")
            return outfile

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download {url}: {e}")
            return None

    def download_gdas_data(self, start_date: str, end_date: str, max_workers: int = 4) -> List[Path]:
        """
        :no-index:

        Download GDAS grib2 files for a specified date range.

        Downloads missing files from NOAA's AWS S3 bucket using parallel requests.

        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            max_workers (int, optional): Maximum number of concurrent downloads. Defaults to 4.

        Returns:
            List[Path]: List of paths to all available files (downloaded + existing)

        Notes:
            - Skips files that already exist locally
            - Uses ThreadPoolExecutor for parallel downloads
            - Shows progress bar during downloads
            - Handles failed downloads gracefully
        """
        current = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        outdir = Path(self.config['input_dir'])
        outdir.mkdir(parents=True, exist_ok=True)

        # Collect download tasks and check existing files
        download_tasks = []
        existing_files = []

        while current <= end:
            for hour in self.config['gdas']['hours']:
                outfile = outdir / f"gdas_{current:%Y%m%d}_{hour:02d}.grib2"
                if outfile.exists():
                    existing_files.append(outfile)
                else:
                    download_tasks.append((current, hour))
            current += timedelta(days=1)

        if not download_tasks:
            logger.info("All files already exist, skipping download")
            return sorted(existing_files)

        logger.info(f"Downloading {len(download_tasks)} files ({len(existing_files)} already exist)")

        # Download missing files
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for date, hour in download_tasks:
                futures.append(
                    executor.submit(self._download_single_file, date, hour, outdir)
                )

            downloaded_files = []
            future_iterator = concurrent.futures.as_completed(futures)

            if has_tqdm:
                future_iterator = tqdm(future_iterator,
                                     total=len(futures),
                                     desc="Downloading GDAS data")
            else:
                logger.info(f"Downloading {len(futures)} GDAS files...")

            for future in future_iterator:
                if future.result():
                    downloaded_files.append(future.result())
                    if not has_tqdm:
                        logger.info(f"Downloaded {len(downloaded_files)}/{len(futures)} files")

        return sorted(existing_files + downloaded_files)

    def process_date_range(self, start_date: str, end_date: str):
        """
        :no-index:

        Process GDAS data files for a date range

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        current = start
        while current <= end:
            logger.info(f"Processing date: {current:%Y-%m-%d}")
            self.config['date'] = current
            try:
                self.process_files()
            except Exception as e:
                logger.error(f"Error processing {current:%Y-%m-%d}: {e}")
                logger.error(traceback.format_exc())
            current += timedelta(days=1)

def combine_dat_files(directory: Path, output_file: Path):
    """Combine multiple daily .dat files into a single combined file.

    Args:
        directory (Path): Directory containing daily .dat files
        output_file (Path): Path where combined file should be written

    Notes:
        - Preserves header from first file
        - Maintains chronological order of data
        - Assumes consistent format across input files
        - Skips duplicate headers from individual files

    Example:
        >>> combine_dat_files(Path('./output'), Path('./output/combined.dat'))
    """
    # Find all .dat files in directory
    dat_files = sorted(directory.glob('gdas_cmaq_*.dat'))
    if not dat_files:
        logger.warning(f"No .dat files found in {directory}")
        return

    logger.info(f"Combining {len(dat_files)} .dat files into {output_file}")

    # Read and combine files
    with open(output_file, 'w') as outf:
        # Copy header from first file (only need once)
        with open(dat_files[0]) as f:
            header_lines = []
            for i in range(3):  # Read first 3 lines (header)
                line = f.readline()
                if i < 2:  # Only write nlat/nlon lines
                    outf.write(line)
                header_lines.append(line)

        # Process all files
        for dat_file in dat_files:
            with open(dat_file) as f:
                # Skip header lines
                for _ in range(3):
                    f.readline()

                # Copy data lines
                for line in f:
                    outf.write(line)

    logger.info(f"Successfully created combined file: {output_file}")

def main():
    """Main program entry point for GDAS data processing.

    Handles:
        1. Command line argument parsing
        2. Configuration loading and validation
        3. Optional GDAS data downloading
        4. Processing of single date or date range
        5. Optional combination of output files

    Raises:
        Various exceptions which are logged with tracebacks
    """
    args = parse_args()
    config = load_config(args)
    processor = GDASProcessor(config)

    # Handle download if requested
    if args.download:
        processor.download_gdas_data(
            config['start_date'].strftime('%Y-%m-%d'),
            config['end_date'].strftime('%Y-%m-%d'),
            args.max_workers
        )

    # Process date range (will handle single date automatically)
    current = config['start_date']
    while current <= config['end_date']:
        logger.info(f"Processing date: {current:%Y-%m-%d}")
        try:
            processor.config['date'] = current  # Set current date for processing
            processor.process_files()
        except Exception as e:
            logger.error(f"Error processing {current:%Y-%m-%d}: {e}")
            logger.error(traceback.format_exc())
        current += timedelta(days=1)

    # After processing all dates, combine .dat files
    if config.get('combine_output', True):  # Make it configurable
        output_dir = Path(config['output_dir'])
        combined_file = output_dir / 'omi_cmaq_combined.dat'
        combine_dat_files(output_dir, combined_file)

if __name__ == '__main__':
    main()
