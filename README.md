# unicode-similarity

TODO

## Getting started

TODO

### Prerequisites

Python version >= 3.5

### Installing

pip install -r requirements.txt

### Usage

#### similarity.py

```
username@host:~/path/to/unicode-similarity$ python3 similarity.py -h
usage: similarity.py [-h] [-i IMAGES] [-o OUTPUT] [-v]

Compute the similarity between Unicode and latin characters by using transfer
learning.

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGES, --images IMAGES
  -o OUTPUT, --output OUTPUT
  -v, --verbose

username@host:~/path/to/unicode-similarity$ python3 similarity.py -i path/to/unicode_database -o path/to/similarity.txt

```
#### threshold.py

```
username@host:~/path/to/unicode-similarity$ python3 threshold.py -h
usage: threshold.py [-h] [-s SIMILARITY] [-i IMAGES] [-t THRESHOLD]
                    [-o OUTPUT] [-v]

Filter Unicode characters based on a given threshold and a similarity matrix

optional arguments:
  -h, --help            show this help message and exit
  -s SIMILARITY, --similarity SIMILARITY
  -i IMAGES, --images IMAGES
  -t THRESHOLD, --threshold THRESHOLD
  -o OUTPUT, --output OUTPUT
  -v, --verbose

```
## Authors

* José Ignacio Escribano Pablos
* Miguel Hernández Boza - @MiguelHzBz
* Alfonso Muñoz Muñoz - @mindcrypt

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
