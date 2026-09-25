from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("getpak")
except PackageNotFoundError:
    from ._version import __version__

from .input import Input
from osgeo import gdal, ogr, osr

__all__ = ["Input", "__version__"]

gdal.UseExceptions()
ogr.UseExceptions()
osr.UseExceptions()
