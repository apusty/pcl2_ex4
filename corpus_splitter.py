#!/usr/bin/env python3
# -*- coding: utf-8  -*-

# Programmiertechniken in der Computerlinguistik II
# Augabe 4
# Autor: Angelina Pustynskaia

import gzip
import random
from typing import BinaryIO

import sys


def split_corpus(infile: BinaryIO, targetdir: str, n: int = 1000):
    # two sets that contain the final chosen documents
    out_set_training = set()
    out_set_test_development = set()

    # count documents in corpus, but only those documents that have at
    # least one sentence
    num_docs = 0
    sentences = 0
    for line in infile:
        utf8_line = line.decode('UTF-8')
        if '<sentence' in utf8_line:
            sentences += 1
        if '<document' in utf8_line and sentences > 0:
            num_docs += 1
            sentences = 0
    print('There are', num_docs, 'documents.')
    infile.seek(0)

    # begin the selection of random samples
    t = 0
    # 2 * 1000, one times 1000 for the test and one times 1000 for the development set
    to_take = 2 * n
    sentences = []
    for line in infile:
        utf8_line = line.decode('UTF-8')
        if '<document' in utf8_line and len(sentences) > 0:
            # this formula is from the algorithm and selects documents randomly
            if (num_docs - t) * random.random() >= to_take - len(out_set_test_development):
                out_set_training.add(' '.join(sentences))
                t += 1
            elif len(out_set_test_development) < to_take:
                # this document is chosen for test or development
                out_set_test_development.add(' '.join(sentences))
                t += 1
            else:
                out_set_training.add(' '.join(sentences))
                t += 1
            sentences = []
        if '<sentence' in utf8_line:
            sentences.append(utf8_line.strip()[10:-11])

    # finally, split test and development randomly into two sets of 1000 each
    out_set_test = set(random.sample(out_set_test_development, n))
    out_set_development = out_set_test_development.copy()
    out_set_development = out_set_development.difference(out_set_test)

    print('There are', len(out_set_training), 'documents in the training set.')
    print('There are', len(out_set_development), 'documents in the development set.')
    print('There are', len(out_set_test), 'documents in the test set.')

    # and store everything to the output directory
    with open(targetdir + '/abstracts.txt.training.gz', 'wb') as of:
        corpus = '\n'.join(out_set_training)
        of.write(gzip.compress(corpus.encode('UTF-8')))
    with open(targetdir + '/abstracts.txt.test.gz', 'wb') as of:
        corpus = '\n'.join(out_set_test)
        of.write(gzip.compress(corpus.encode('UTF-8')))
    with open(targetdir + '/abstracts.txt.development.gz', 'wb') as of:
        corpus = '\n'.join(out_set_development)
        of.write(gzip.compress(corpus.encode('UTF-8')))


if __name__ == '__main__':
    with gzip.open(sys.argv[1], mode='rb') as infile:
        split_corpus(infile, 'Korpusdaten')
