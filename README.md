# ter_converter
A utility for converting Terragen height map .TER files to .EXR files

[Link to official .TER format specification](https://planetside.co.uk/wiki/index.php?title=Terragen_.TER_Format)

## Install:


download or clone repository 

pip3 install -r requirements.txt

imageio_download_bin freeimage # [gets the .EXR binaries](https://imageio.readthedocs.io/en/stable/format_exr-fi.html) for imageio (used for image export)

## Usage:
```
usage: python ter_converter.py [-h] -i INPUT_FILE_PATH -o OUTPUT_FILE_PATH
                               [use_base_height] [use_height_scale]
                               [convert_log_scale]

positional arguments:
  use_base_height      use base height
  use_height_scale     use height scale
  convert_log_scale    convert log scale

optional arguments:
  -h, --help           show this help message and exit
  -i INPUT_FILE_PATH   input file path
  -o OUTPUT_FILE_PATH  output file path
  
Example: python ter_converter.py -i some_terragen_file.ter -o my_new_heightmap.exr
```

To export .TER format height maps from Terragen create a Heightfield Generate node, set the resolution, right click on the node and select "Save File As..."  

If you need support for other formats please feel free to submit and issue or pull request.
