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


def remove_extension(x): return x.split('.')[0]


def file_exists(path):
    return Path(path).is_file()


def dir_exists(path):
    return Path(path).is_dir()


def print_error(type, file):
    print(FileNotFoundError(errno.ENOENT,
                            'The {} {} does not exist'.format(type, file)))


def similarity_pairs(dir, output, verbose=False):
    U, L, unicode_characters, latin_characters = load_data(dir, verbose)
    # latin_characters = [format(i + 32, '05x') for i in range(96)]
    # unicode_characters = sorted(os.listdir(dir))

    model = VGG16(include_top=False, weights='imagenet')

    if verbose:
        print('Predicting Unicode characters...')
        unicode_predicts = model.predict(U, verbose=1)
        print('Predicting latin characters...')
        latin_predicts = model.predict(L, verbose=1)
    else:
        unicode_predicts = model.predict(U)
        latin_predicts = model.predict(L)


    with open(output, 'a') as file:
        to_file = ' ' + ' '.join(unicode_characters) + '\n'
        file.write(to_file)

    for i, latin_character in enumerate(latin_characters):
        with open(output, 'a') as file:
            to_file = latin_character
            for j, unicode_chracter in enumerate(unicode_characters):
                # latin_path = os.path.join(dir, latin_character) + ".png"

                # latin_img = load_img(latin_path)

                # unicode_path = os.path.join(dir, unicode_chracter)
                # unicode_img = load_img(unicode_path)

                latin_pred = latin_predicts[i].reshape(1, -1)
                unicode_pred = unicode_predicts[j].reshape(1, -1)

                sim = similarity(latin_pred, unicode_pred)
                to_file = to_file + ' ' + str(sim)
                if verbose:
                    print(('Similarity between '
                          '{} and {}: {}').format(latin_character,
                                                  remove_extension(
                                                    unicode_chracter), sim))
            to_file = to_file + '\n'
            file.write(to_file)
            to_file = ''


def similarity(x, y):
    return np.asscalar(cosine_similarity(x, y))

def load_data(dir, verbose=False):
    latin_characters = ['{}.png'.format(format(i + 32, '05x')) for i in range(96)]

    num_unicode_samples = 38800
    num_latin_samples = 96

    U = np.empty((num_unicode_samples, 224, 224, 3), dtype='uint8')
    L = np.empty((num_latin_samples, 224, 224, 3), dtype='uint8')

    latin_characters_count = 0
    unicode_characters = sorted(os.listdir(dir))
    for i, name in enumerate(unicode_characters):
        # print(im_name)
        path = os.path.join(dir, name)
        input_im = load_img(path)
        U[i,:,:,:] = input_im
        if verbose:
            print('Loading image {}'.format(name))
        if(name in latin_characters):
            L[latin_characters_count,:,:,:] = input_im
            latin_characters_count = latin_characters_count + 1
    return U, L, list(map(remove_extension,unicode_characters)), list(map(remove_extension,latin_characters))


def load_img(path):
    img = image.load_img(path, target_size=(224, 224),
                         grayscale=False, interpolation='bilinear')
    x = image.img_to_array(img)
    x = preprocess_input(x)
    # x = np.expand_dims(x, axis=0)
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
