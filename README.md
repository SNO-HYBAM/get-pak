[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21372746-blue.svg)](https://doi.org/10.5281/zenodo.21372746)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 
## GET-Pak

**G**éosciences **E**nvironnement **T**oulouse – **P**rocessing and **A**nalysis Wor**k**bench

GET-Pak is an open-source Python toolbox for reproducible inland-water quality research.

It converts atmospherically corrected Sentinel-2 MSI reflectance products (especially GRS NetCDF outputs), into Level-2B water-quality maps such as suspended particulate matter, turbidity and chlorophyll-a. It also extracts statistics over user-defined regions of interest (ROI) in shapefile format, builds time series, and prepares satellite–in situ matchups for validation.

GET-Pak is designed for both interactive Jupyter workflows and automated batch processing (CLI), making it suitable for single-scene exploration, regional monitoring, and large image collections on local machines or HPC systems.

Citation will be possible once article submission process is complete, auxiliary data for reproducibility purposes is available at Zenodo under the link: https://doi.org/10.5281/zenodo.21372746 containing the ROI file liangzi_lake_epsg32650.shp, 3 GRS images and 3 pre-computed water masks so the user can test-run the program and generate an example report.

```plaintext
            _..._
          .'     '.      _
         /    .-""-\   _/ \ 
       .-|   /:.   |  |   | 
       |  \  |:.   /.-'-./ 
       | .-'-;:__.'    =/  ,ad8888ba,  88888888888 888888888888                          88
       .'=  *=|CNES _.='  d8"'    `"8b 88               88                               88
      /   _.  |    ;     d8'           88               88                               88
     ;-.-'|    \   |     88            88aaaaa          88        8b,dPPYba,  ,adPPYYba, 88   ,d8
    /   | \    _\  _\    88      88888 88"""""          88 aaaaaa 88P'    "8a ""     `Y8 88 ,a8"
    \__/'._;.  ==' ==\   Y8,        88 88               88 """""" 88       d8 ,adPPPPP88 8888[
    /|\  /|\ \    \   |   Y8a.    .a88 88               88        88b,   ,a8" 88,    ,88 88`"Yba,
   / | \/ | \/    /   /    `"Y88888P"  88888888888      88        88`YbbdP"'  `"8bbdP"Y8 88   `Y8a
  /  | || |  /-._/-._/                                            88
             \   `\  \                                            88
              `-._/._/
```
### Setup
> [!IMPORTANT]
> GDAL is a requirement for the installation, therefore, usage of a conda environment ([Anaconda.org](https://www.anaconda.com/products/individual)) is **STRONGLY** recommended. Unless you know what you are doing (-:

## Installation
Create a Conda environment using python 3.10 (compatible for both windows and linux):
```
conda create --name gpk310 python=3.10
```
Activate your conda env:
```
conda activate gpk310
```
With your conda env activated, install `GDAL` before installing `getpak` to avoid dependecy errors, note that you should not specify the channel using -c in this step:
```
conda install gdal
```
Once `GDAL` is installed, clone `getpak` repository to any desired location, enter the folder and install required the dependencies:
```
pip install -r requirements.txt
```
Aditional dependency libraries note present in the requirements.txt also need to be installed for OS-compatibility reasons:
```
conda install h5py libgdal-netcdf
```
Install the package:
```
pip install -e .
```
Done.

> [!TIP]
> You can test-run GET-Pak with the files provided [here](https://doi.org/10.5281/zenodo.21372746).

## BEFORE RUNNING

⚠️ Be sure that settings.ini file is adapted to your needs before launching the program!

Run the full settings-driven workflow:
```
python main.py run
```
Run only the L2B processing step:
```
python main.py l2b
```

Run only the report/time-series extraction step:
```
python main.py report
```

The automation module can also be launched directly:
```
python -m getpak.automation
```

## Related research

GET-Pak's current release integrates methodology from the following articles:

Harmel, T., Chami, M., Tormos, T., Reynaud, N., Danis, P.-A., 2018. Sunglint correction of the Multi-Spectral Instrument (MSI)-SENTINEL-2 imagery over inland and sea waters from SWIR bands. Remote Sensing of Environment 204, 308–321. [https://doi.org/10.1016/j.rse.2017.10.022](https://doi.org/10.1016/j.rse.2017.10.022)

Tavares, M.H., Guimarães, D., Roussillon, J., Baute, V., Cucherousset, J., Boulêtreau, S., Martinez, J.-M., 2025. A Framework to Retrieve Water Quality Parameters in Small, Optically Diverse Freshwater Ecosystems Using Sentinel-2 MSI Imagery. Remote Sensing 17, 2729. [https://doi.org/10.3390/rs17152729](https://doi.org/10.3390/rs17152729)

Cordeiro, M.C.R., Martinez, J.-M., Peña-Luque, S., 2021. Automatic water detection from multidimensional hierarchical clustering for Sentinel-2 images and a comparison with Level 2A processors. Remote Sensing of Environment 253, 112209. [https://doi.org/10.1016/j.rse.2020.112209](https://doi.org/10.1016/j.rse.2020.112209)

