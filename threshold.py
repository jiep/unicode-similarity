from pathlib import Path
import numpy as np
import pickle
import argparse
import errno
import sys


def file_exists(path):
    return Path(path).is_file()


def dir_exists(path):
    return Path(path).is_dir()


def remove_extension(x): return x.split('.')[0]


def print_error(type, file):
    print(FileNotFoundError(errno.ENOENT,
                            'The {} {} does not exist'.format(type, file)))


def calculate_threshold(similarity, output='confusables.pickle',
                        threshold=0.8, verbose=False):

    lines = [line.rstrip('\n') for line in open(similarity)]

    unicode_characters = np.asarray(lines[0].split(' ')[1:])

    data = {}
    data['threshold'] = threshold
    data['characters'] = {}
    for l in lines[1:]:
        line = l.split(' ')
        latin = line[0]
        del line[0]
        similarity_row = np.asarray(line, dtype=np.float)
        indexes = np.where(similarity_row >= threshold)
        data['characters'][latin] = unicode_characters[np.asarray(indexes[0])]\
            .tolist()

        chars = unicode_characters[np.asarray(indexes[0])].tolist()

        if(verbose):
            print('[{}] {}: {}'.format(len(chars), latin, ','.join(chars)))

    with open(output, 'wb') as f:
        pickle.dump(data, f)


def main():
    parser = argparse.ArgumentParser(description='Filter Unicode characters '
                                                 'based on a given threshold '
                                                 'and a similarity matrix')

    parser.add_argument('-s', '--similarity', default='similarities.txt')
    parser.add_argument('-t', '--threshold', default=0.8, type=float)
    parser.add_argument('-o', '--output', default='confusables.pickle')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    similarity = args.similarity
    threshold = args.threshold
    output = args.output
    verbose = args.verbose

    if not file_exists(similarity):
        print_error('file', similarity)
        sys.exit(1)

    calculate_threshold(similarity, output, threshold, verbose)


if __name__ == '__main__':
    main()
