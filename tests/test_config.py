from datetime import datetime

import pytest
from gdas_cmaqprep import load_config
from gdas_cmaqprep.create_gdas_omi import parse_args


def test_load_config(temp_config_file):
    args = parse_args(["--config", temp_config_file.as_posix()])
    config = load_config(args)
    assert config["nlat"] == 720
    assert config["nlon"] == 1440
    assert isinstance(config["start_date"], datetime)
    assert isinstance(config["end_date"], datetime)
    assert config["gdas"]["hours"] == [12]


def test_invalid_config():
    args = parse_args([])
    with pytest.raises(FileNotFoundError):
        load_config(args)
