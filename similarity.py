import numpy as np
import os
import sys
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.applications import VGG16
from sklearn.metrics.pairwise import cosine_similarity
import argparse
from pathlib import Path
import errno


def file_exists(path):
    return Path(path).is_file()


def dir_exists(path):
    return Path(path).is_dir()


def print_error(type, file):
    print(FileNotFoundError(errno.ENOENT,
                            'The {} {} does not exist'.format(type, file)))


def similarity_pairs(dir, output, verbose=False):
    latin_characters = [format(i + 32, '05x') for i in range(96)]
    unicode_characters = os.listdir(dir)

    latin_characters_count = 0

    model = VGG16(include_top=False, weights='imagenet')

    for i, latin_character in enumerate(latin_characters):
        with open(output, 'a') as file:
            to_file = ' ' + ' '.join(unicode_characters) + '\n'
            file.write(to_file)
            to_file = latin_character
            for j, unicode_chracter in enumerate(os.listdir(dir)):
                latin_path = os.path.join(dir, latin_character) + ".png"

                latin_img = load_img(latin_path)

                unicode_path = os.path.join(dir, unicode_chracter)
                unicode_img = load_img(unicode_path)

                latin_pred = model.predict(latin_img).reshape(1, -1)
                unicode_pred = model.predict(unicode_img).reshape(1, -1)

                sim = similarity(latin_pred, unicode_pred)
                to_file = to_file + ' ' + str(sim)
                if verbose:
                    print(('Similarity between '
                          '{} and {}: {}').format(latin_character,
                                                  unicode_chracter, sim))
            to_file = to_file + '\n'
            file.write(to_file)
            to_file = ''


def similarity(x, y):
    return np.asscalar(cosine_similarity(x, y))


def load_img(path):
    img = image.load_img(path, target_size=(224, 224),
                         grayscale=False, interpolation='bilinear')
    x = image.img_to_array(img)
    x = preprocess_input(x)
    x = np.expand_dims(x, axis=0)
    return x


def main():
    parser = argparse.ArgumentParser(description='Compute the similarity '
                                                 'between Unicode and latin '
                                                 'characters by using '
                                                 'transfer learning.')

    parser.add_argument('-i', '--images', default='images')
    parser.add_argument('-o', '--output', default='similarities.txt')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    images = args.images
    output = args.output
    verbose = args.verbose

    if file_exists(output):
        print('Removing {}...'.format(output))
        os.remove(output)

    if not dir_exists(images):
        print_error('directory', images)
        sys.exit(1)

    similarity_pairs(images, output, verbose)


if __name__ == '__main__':
    main()
