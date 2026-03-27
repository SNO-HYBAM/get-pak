from .input import Input
from osgeo import gdal, ogr, osr


__all__ = ['Input']

gdal.UseExceptions()
ogr.UseExceptions()
osr.UseExceptions()