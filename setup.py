from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gdas-cmaqprep",
    version="0.1.0",
    author="NOAA Air Resources Laboratory",
    author_email="",
    description="A tool for processing GDAS data for CMAQ model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noaa-arl/gdas_cmaqprep",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "xarray>=0.16.0",
        "netCDF4>=1.5.7",
        "grib2io>=1.0.0",
        "pyyaml>=5.4.1",
        "requests>=2.25.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=3.9",
            "mypy>=0.910",
            "sphinx>=4.0",
            "sphinx-rtd-theme",
            "myst-parser",
        ],
        "progress": ["tqdm>=4.61.0"],  # Make progress bar optional
    },
    entry_points={
        "console_scripts": [
            "gdas-cmaqprep=gdas_cmaqprep.cli:main",
        ],
    },
)
