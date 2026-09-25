import os
import re
from setuptools import setup, find_packages

__package__ = 'getpak'

_version_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'getpak', '_version.py')
with open(_version_path, encoding='utf-8') as _version_file:
    __version__ = re.search(r'__version__\s*=\s*[\"\']([^\"\']+)', _version_file.read()).group(1)

short_description = 'Raster and vector manipulation toolbox for reproducible water quality research.'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=__package__,
    version=__version__,
    url="https://github.com/SNO-HYBAM/get-pak",
    packages=find_packages(include=["getpak", "getpak.*"]),
    py_modules=['main'],
    python_requires='>=3.10,<3.14',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        'getpak': ['data/*.json', 'data/*.ini'],
    },
    include_package_data=True,

    license='MIT',
    author='David Guimaraes',
    author_email='dvdgmf@gmail.com',
    description=short_description,
    entry_points={
        'console_scripts': ['getpak=main:main'],
    },
    install_requires=[
        'affine',
        'dask',
        'fiona',
        'geopandas',
        'h5py',
        'h5netcdf',
        'netCDF4',
        'numpy',
        'openpyxl',
        'pandas',
        'Pillow',
        'rasterio',
        'rasterstats==0.19.0',
        'rioxarray',
        'scikit-learn',
        'shapely',
        'xarray==2023.12.0',
    ],
    extras_require={
        'test': ['pytest>=7,<9'],
    },
)
