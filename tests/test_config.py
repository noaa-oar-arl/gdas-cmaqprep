import pytest
from gdas_cmaqprep.config import load_config
from datetime import datetime

def test_load_config(temp_config_file):
    config = load_config(temp_config_file)
    assert config['nlat'] == 720
    assert config['nlon'] == 1440
    assert isinstance(config['start_date'], datetime)
    assert isinstance(config['end_date'], datetime)
    assert config['gdas']['hours'] == [12]

def test_invalid_config():
    with pytest.raises(ValueError):
        load_config("nonexistent.yml")
