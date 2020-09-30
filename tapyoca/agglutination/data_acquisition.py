import re
import pkgutil
import os
from functools import partial

import requests

standard_lib_dir = os.path.dirname(os.__file__)


def is_standard_lib_path(path):
    return path.startswith(standard_lib_dir)


def standard_lib_module_names(is_standard_lib_path=is_standard_lib_path,
                              name_filt=lambda name: not name.startswith('_')):
    return filter(name_filt, (module_info.name for module_info in pkgutil.iter_modules()
                              if is_standard_lib_path(module_info.module_finder.path)))


only_letters_p = re.compile('[a-zA-Z]+')

urls = {
    'git370077': 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt',
    'corncob': 'http://www.mieliestronk.com/corncob_lowercase.txt',
    # Note: corncob favors british spelling. Does not contain "a" (?!?)
    'jlawler': 'http://www-personal.umich.edu/~jlawler/wordlist',
    'mit': 'https://www.mit.edu/~ecprice/wordlist.10000',
    'google1000': 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa.txt'
}


def get_words(url=urls['google1000'], min_word_size=2):
    """Gets a list of words (only uninterrupted sequences of letters) from a url source"""
    import urllib.request

    with urllib.request.urlopen(url) as r:
        content = (r.status == 200) and r.read().decode()
    if content:
        # only keep words that are uninterru¬pted letter sequences of length at least 2, and lower case these
        words = {word.lower() for word in only_letters_p.findall(content) if len(word) >= min_word_size}
        return words
    else:
        raise RuntimeError(f"Something went wrong. I got a status code of {r.status}")


# adding attributes to get_words for easier access to url source
for name, url in urls.items():
    setattr(get_words, f"{name}", partial(get_words, url=url))


def _acquire_data():
    words = get_words.google1000() & get_words.corncob()
    with open('words_8116.csv', 'w') as fp:
        fp.write('\n'.join(sorted(words)))

    py_names = sorted(standard_lib_module_names())
    with open('standard_lib_module_names.csv', 'w') as fp:
        fp.write('\n'.join(py_names))

# words = (get_words_from_csv_url(urls['google1000'])
#          & get_words_from_csv_url(urls['corncob']))
# # words = get_words_from_csv_url(urls['huge'])
# sorted_words = sorted(words)
# len(words)
