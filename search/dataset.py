#!/usr/bin/env python3

import collections
import os
from typing import List

Score = collections.namedtuple("Score", "total, content, location, page_rank")
Rank = collections.namedtuple("Rank", "url, score")


class Page:
    def __init__(self,
                 url: str,
                 name: str,
                 words: List[int],
                 links: List[str],
                 page_rank: float=1.0) -> None:
        self._url = url
        self._name = name
        self._words = words
        self._links = links
        self._page_rank = page_rank

    @property
    def url(self) -> str:
        return self._url

    @property
    def name(self) -> str:
        return self._name

    @property
    def words(self) -> List[int]:
        return self._words

    @property
    def links(self) -> List[str]:
        return self._links

    @property
    def page_rank(self) -> float:
        return self._page_rank

    @page_rank.setter
    def page_rank(self, value: float) -> None:
        self._page_rank = value


class Dataset:
    _page_rank_iterations = 20
    _page_rank_damping_factor = 0.85
    _page_rank_minimum_value = 0.15

    def __init__(self, words_path: str, links_path: str,
                 name_format: str) -> None:
        """
        Read a dataset of words and links.

        Args:
            words_path: base path to the directory of words.
            links_path: base path to the directory of links.
            name_format: Format that specifies how a given page is linked to.
        """
        self._word_map = {}  # type: Dict[str, int]
        self._pages = []  # type: List[Page]

        for dirpath, _, filenames in os.walk(words_path):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                name = name_format.format(path=path, filename=filename)
                words = self._get_words(path)
                common_path = path[len(words_path) + 1:]
                links = self._get_links(os.path.join(links_path, common_path))
                self._pages.append(Page(path, name, words, links))

        self._calculate_page_rank()

    def search(self, query: str) -> List[Rank]:
        """
        Search the dataset.

        Args:
            query: The query to search for.

        Returns:
            List[Rank]: A list of sorted pages.
        """
        content_scores = []
        location_scores = []

        # Calculate scores for every page
        for page in self._pages:
            content_scores.append(self._get_content_score(page, query))
            location_scores.append(self._get_location_score(page, query))

        # Normalize the scores
        self._normalize(content_scores, False)
        self._normalize(location_scores, True)

        # Return the results sorted by the total score
        result = []
        elements = zip(self._pages, content_scores, location_scores)
        for page, content_score, location_score in elements:
            location_score *= 0.8
            page_rank = page.page_rank * 0.5
            score = Score(
                total=content_score + location_score + page_rank,
                content=content_score,
                location=location_score,
                page_rank=page_rank)
            result.append(Rank(page.url, score))
        result.sort(key=lambda r: r.score.total, reverse=True)
        return result

    def _calculate_page_rank(self) -> None:
        # Calculate page rank for every page
        for _ in range(self._page_rank_iterations):
            for target in self._pages:
                page_rank = 0.0
                for other in self._pages:
                    try:
                        other.links.index(target.name)
                        page_rank += other.page_rank / len(other.links)
                    except ValueError:
                        pass
                target.page_rank = self._page_rank_damping_factor * page_rank \
                    + self._page_rank_minimum_value

        # Normalize the ranks
        page_ranks = [page.page_rank for page in self._pages]
        self._normalize(page_ranks, False)
        for page in self._pages:
            page.page_rank = page_ranks.pop(0)

    def _get_content_score(self, page: Page, query: str) -> float:
        """
        Calculate content score.

        Args:
            page: Target page.
            query: Search query.

        Returns:
            float: Content score.
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
        word = word.lower()

        word_id = self._word_map.get(word, -1)
        if word_id != -1:
            return word_id

        word_id = len(self._word_map)
        self._word_map[word] = word_id
        return word_id

    @staticmethod
    def _get_links(path: str) -> List[str]:
        link_list = []
        with open(path, "r") as f:
            for line in f.readlines():
                stripped = line.strip()
                if stripped:
                    link_list.append(stripped)
        return link_list

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
