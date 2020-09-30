import re
import inspect
import importlib
from itertools import chain

from tapyoca.tapyoca.agglutination import mjoin
from tapyoca.tapyoca.agglutination.partitions import WordPartitions

only_letters_p = re.compile('[a-zA-Z]+')

with open(mjoin('standard_lib_module_names.csv'), 'rt') as fp:
    list_of_builtin_module_names = sorted(set(fp.read().split('\n')) - {'this'})


def yield_names(source, modules_visited=None, max_recursions=4):
    if max_recursions <= 0:
        return
    modules_visited = modules_visited or set()

    if inspect.ismodule(source):
        if source in modules_visited:
            return
        else:
            modules_visited.add(source)

    if callable(source) or inspect.ismodule(source):
        for attr_name in filter(only_letters_p.match, dir(source)):
            yield attr_name
            try:
                attr_val = getattr(source, attr_name)
                yield from yield_names(attr_val, modules_visited, max_recursions - 1)
            except Exception:  # blanket catching to ignore stuff I don't want to handle
                pass

        if callable(source):
            try:  # try this if source has a signature
                yield from filter(only_letters_p.match, inspect.signature(source).parameters)
            except Exception:
                pass


def gluglu_words_from_module(module, words=None):
    wp = WordPartitions(words)
    return set(filter(wp.partition_score_greater_than_one,
                      filter(wp.is_word_agglutination,
                             filter(str.islower, set(yield_names(module)))
                             )
                      )
               ) - wp.words


def get_gluglus_from_standard_lib(words=None, onerror='print'):

    def gen():
        for module_name in list_of_builtin_module_names:
            try:
                module = importlib.import_module(module_name)
                yield gluglu_words_from_module(module, words)
            except ModuleNotFoundError as e:
                if onerror == 'print':
                    print(f"{module_name}: {e}")

    return set(chain.from_iterable(gen()))


