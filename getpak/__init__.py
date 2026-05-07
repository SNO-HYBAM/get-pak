from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("getpak")
except PackageNotFoundError:
    __version__ = "unknown"

from .input import Input
from osgeo import gdal, ogr, osr

__all__ = ["Input", "__version__"]

gdal.UseExceptions()
ogr.UseExceptions()
osr.UseExceptions()