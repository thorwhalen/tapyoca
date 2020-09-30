import re
from heapq import heappush, heappushpop

from tapyoca.tapyoca.agglutination import mjoin


def get_default_words():
    with open(mjoin('words_8116.csv'), 'rt') as fp:
        words = set(fp.read().split('\n'))

    return words


class KeepMaxK(list):
    def __init__(self, k):
        super(self.__class__, self).__init__()
        self.k = k

    def push(self, item):
        if len(self) >= self.k:
            heappushpop(self, item)
        else:
            heappush(self, item)


class WordPartitions:
    def __init__(self, words=None, max_n_inner_words=4):
        """See data_acquisition module for ways to acquire different sets of words"""
        if words is None:
            words = get_default_words()
        word_disjunction = '(' + '|'.join(sorted(words)) + ')'
        pattern_matching_word_agglutinations = '|'.join(f"({word_disjunction * n_inner_words})$"
                                                        for n_inner_words in list(range(2, max_n_inner_words + 1)))
        self.agglutination_re = re.compile(pattern_matching_word_agglutinations, re.IGNORECASE)

        self.words = set(words)

    def word_partitions(self, word: str, path=()):
        """
        >>> wp = WordPartitions()
        >>> assert list(wp.word_partitions('representation')) == [
        ...     ('re', 'pre', 'sent', 'at', 'ion'),
        ...     ('re', 'present', 'at', 'ion'),
        ...     ('re', 'presentation'),
        ...     ('rep', 're', 'sent', 'at', 'ion'),
        ...     ('represent', 'at', 'ion'),
        ...     ('representation',)
        ... ]
        """
        for i in range(1, len(word)):
            subword = word[:i]
            if subword in self.words:
                yield from self.word_partitions(word[i:], path + (subword,))
        if word in self.words:
            yield path + (word,)

    def get_top_partitions(self, n=10):
        km = KeepMaxK(n)
        for word in self.words:
            partitions = list(self.word_partitions(word))
            km.push((len(partitions), partitions))
        return km

    def partition_score(self, word):
        return len(list(self.word_partitions(word)))

    gluglu = partition_score

    def partition_score_greater_than_one(self, word):
        for i, w in enumerate(self.word_partitions(word)):
            if i > 0:
                return True
        return False

    def is_word_agglutination(self, word):
        """
        >>> wp = WordPartitions()
        >>> assert wp.is_word_agglutination('is') is False  # one word doesn't match
        >>> assert wp.is_word_agglutination('isupper') is True  # two words does
        >>> assert wp.is_word_agglutination('isupperbound') is True  # three as well
        >>> assert wp.is_word_agglutination('isqqq') is False  # partial matches... don't match

        """
        return bool(self.agglutination_re.match(word))

    def nice_string_for_gluglus(self, word_partitions):
        def gen():
            for w in sorted(word_partitions):
                yield f"{w}"
                for p in self.word_partitions(w):
                    yield f'\t{" ".join(p)}'

        return '\n'.join(gen())
