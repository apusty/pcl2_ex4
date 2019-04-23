#!/usr/bin/env python3
# -*- coding: utf-8  -*-

# Programmiertechniken in der Computerlinguistik II
# Augabe 4
# Autor: Angelina Pustynskaia

from typing import Iterable


def longest_substrings(x: str, y: str) -> Iterable[str]:
    # make both lower case
    x = x.lower()
    y = y.lower()
    n = len(x)
    m = len(y)
    # build an empty matrix (from lecture slide 21)
    d = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    # assign the value to each cell (+ 1 from the diagonal one if the two letters are the same)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if x[i - 1] == y[j - 1]:
                d[i][j] = d[i - 1][j - 1] + 1

    # take the maximal values from the matrix, and store the positions
    max_len = 0
    max_pos = []
    # only go through one of the words (x) as the suffixes are the same
    for i in range(n + 1):
        if max(d[i]) > max_len:
            max_len = max(d[i])
            max_pos = [i]
        elif max(d[i]) == max_len:
            max_pos.append(i)
    # if the maximal value found is 0, this means there is no common suffix
    if max_len == 0:
        return None
    else:
        return [x[pos-max_len:pos] for pos in max_pos]


if __name__ == '__main__':
    print(longest_substrings('Tod', 'Leben'))
    print(longest_substrings('Haus', 'Maus'))
    print(longest_substrings('mozart','mozzarella'))
    print(longest_substrings('keep the interface!', 'KeEp ThE iNtErFaCe!'))
