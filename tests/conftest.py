import pytest
from pathlib import Path
import tempfile
import yaml


@pytest.fixture
def test_config():
    return {
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "input_dir": "input",
        "output_dir": "output",
        "nlat": 720,
        "nlon": 1440,
        "lat_border": 0.125,
        "use_prev_date": True,
        "gdas": {
            "hours": [12],
            "base_url": "https://noaa-gfs-bdp-pds.s3.amazonaws.com",
            "file_pattern": "gfs.t{hour:02d}z.pgrb2.0p25.anl",
        },
    }


@pytest.fixture
def temp_config_file(test_config):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
        yaml.dump(test_config, f)
    yield Path(f.name)
    Path(f.name).unlink()


@pytest.fixture
def temp_workspace():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
