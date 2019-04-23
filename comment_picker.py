#!/usr/bin/env python3
# -*- coding: utf-8  -*-

# Programmiertechniken in der Computerlinguistik II
# Augabe 4
# Autor: Angelina Pustynskaia

import bz2
import json
from typing import BinaryIO

import sys


def mk_meme_corpus(infile: BinaryIO, outfile: str, min_score: int = 100,
                   min_len: int = 1, max_len: int = 50):
    out_set = set()

    for line in infile:
        utf8_line = line.decode('UTF-8')
        json_line = json.loads(utf8_line)
        text = json_line['body']
        score = json_line['score']
        if min_len < len(text) < max_len and score > min_score:
            out_set.add(text)

    with open(outfile, 'wb') as of:
        corpus = '\n'.join(out_set)
        of.write(bz2.compress(corpus.encode('UTF-8')))


if __name__ == '__main__':
    with bz2.open(sys.argv[1], mode='r') as infile:
        mk_meme_corpus(infile, 'Korpusdaten/out.bz2')
