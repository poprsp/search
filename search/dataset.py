#!/usr/bin/env python3

import collections
import os
from typing import List

Page = collections.namedtuple("Page", "url, words")


class Dataset:
    def __init__(self, basedir: str) -> None:
        self._word_map = {}  # type: Dict[str, int]
        self._pages = []  # type: List[Page]

        for dirpath, _, filenames in os.walk(basedir):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                words = self._get_words(path)
                self._pages.append(Page(path, words))

    def _get_words(self, path: str) -> List[int]:
        word_list = []
        with open(path, "r") as f:
            for line in f.readlines():
                for word in line.split():
                    word_list.append(self._get_word_id(word))
        return word_list

    def _get_word_id(self, word: str) -> int:
        word_id = self._word_map.get(word)
        if word_id:
            return word_id

        word_id = len(self._word_map)
        self._word_map[word] = word_id
        return word_id
