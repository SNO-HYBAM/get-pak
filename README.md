## GET-pak
**G**éosciences **E**nvironnement **T**oulouse - **P**rocessing and **a**nalysis Wor**k**bench

GETpak aims to provide tools for Sentinel-2 and Sentinel-3 mission data in GeoTIFF and NetCDF formats using vector polygons to extract and manipulate data in order to facilitate and automate analysis and validation tasks.

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
⚠️ GDAL is a requirement for the installation, therefore, 
usage of a conda environment 
([Anaconda.org](https://www.anaconda.com/products/individual)) 
is strongly recommended. Unless you know what you are doing (-:

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
Check if the settings.ini file is adapted to your needs before launching the program, then:
```
python -m getpak.automation
```
