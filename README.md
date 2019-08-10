
## Micropython Uploader

### The script can:

* Recursively bypass the current directory
* Download detected files to mk. It was decided that you should push only `.py` files.
* Delete all files with mk (ps directory is also a file)

## Installation

On MacOS or Linux, in a terminal run the following command (assuming
Python 3):

    pip3 install --user micropython-uploader

On Windows, do:

    pip install micropython-uploader

## Usage

In terminal run:
    
    mploader

### Requirements:

* ampy

        pip3 install ampy
        

* `micropython` as firmware for microcontroller
