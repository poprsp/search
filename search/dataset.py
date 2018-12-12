#!/usr/bin/env python3

import collections
import os
from typing import List

Page = collections.namedtuple("Page", "url, words")
Rank = collections.namedtuple("Rank", "page, score")


class Dataset:
    def __init__(self, basedir: str) -> None:
        self._word_map = {}  # type: Dict[str, int]
        self._pages = []  # type: List[Page]

        for dirpath, _, filenames in os.walk(basedir):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                words = self._get_words(path)
                self._pages.append(Page(path, words))

    def search(self, query: str) -> List[Rank]:
        """
        Search the dataset.

        Args:
            query: The query to search for.

        Returns:
            List[Rank]: A list of sorted pages.
        """
        frequency_scores = []
        location_scores = []

        # Calculate scores for every page
        for page in self._pages:
            frequency_scores.append(self._get_frequency_score(page, query))
            location_scores.append(self._get_location_score(page, query))

        # Normalize the scores
        self._normalize(frequency_scores, False)
        self._normalize(location_scores, True)

        # Return the results sorted by score
        result = [
            Rank(page, frequency_score + 0.5 * location_score)
            for page, frequency_score, location_score in zip(
                self._pages, frequency_scores, location_scores)
        ]
        result.sort(key=lambda r: r.score, reverse=True)
        return result

    def _get_frequency_score(self, page: Page, query: str) -> float:
        """
        Calculate frequency score.

        Args:
            page: Target page.
            query: Search query.

        Returns:
            float: Frequency score.
        """
        score = 0
        for word in query.split():
            word_id = self._get_word_id(word)
            for w in page.words:
                if w == word_id:
                    score += 1
        return score

    def _get_location_score(self, page: Page, query: str) -> float:
        """
        Calculate location score.

        Args:
            page: Target page.
            query: Search query.

        Returns:
            float: Location score.
        """
        score = 1
        for word in query.split():
            try:
                score += page.words.index(self._get_word_id(word))
            except ValueError:
                score += 99999
        return score

    def _get_words(self, path: str) -> List[int]:
        word_list = []
        with open(path, "r") as f:
            for line in f.readlines():
                for word in line.split():
                    word_list.append(self._get_word_id(word))
        return word_list

    def _get_word_id(self, word: str) -> int:
        word_id = self._word_map.get(word, -1)
        if word_id != -1:
            return word_id

        word_id = len(self._word_map)
        self._word_map[word] = word_id
        return word_id

    @staticmethod
    def _normalize(scores: List[float], small_is_better: bool) -> None:
        """
        Normalize a list of scores.

        Args:
            scores: Scores to normalize.
            small_is_better: If a small score is better than a high.
        """
        if small_is_better:
            min_score = min(scores)
            for i, score in enumerate(scores):
                scores[i] = min_score / max(score, 0.00001)
        else:
            max_score = max(scores)
            for i, score in enumerate(scores):
                scores[i] = score / max(max_score, 0.00001)
