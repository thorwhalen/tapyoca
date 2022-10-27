import os

pkg_folder = os.path.dirname(__file__)
mjoin = lambda *p: os.path.join(pkg_folder, *p)

from partitions import WordPartitions
from py_names import get_gluglus_from_standard_lib, yield_names, list_of_builtin_module_names, gluglu_words_from_module

