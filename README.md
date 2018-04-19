# V2D-similarity

This project extract all the unicode image features to compare and create a confusables file that we used in the CLI. More in detail, we use VGG16 model, with weights pre-trained on ImageNet.

We applied the neural network to extract the features of the Basic Latin Unicode and the others blocks and generate a similarities vectors. Then, we process with cosine function this vectors to extract the coefficient of similarity between images. Finally, this process generate a matrix with all the comparatives and its used in the CLI.

## Getting started

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

username@host:~/path/to/unicode-similarity$ python3 similarity.py -i path/to/unicode_database -o path/to/similarities.txt

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
  -t THRESHOLD, --threshold THRESHOLD
  -o OUTPUT, --output OUTPUT
  -v, --verbose

username@host:~/path/to/unicode-similarity$ python3 similarity.py -o path/to/confusables.pickle -s path/to/similarities.txt
```
## Authors

* José Ignacio Escribano Pablos
* Miguel Hernández Boza - @MiguelHzBz
* Alfonso Muñoz Muñoz - @mindcrypt

## Contributing

Any collaboration is welcome!

There're many tasks to do.You can check the [Issues](https://github.com/jiep/unicode/issues) and send us a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
