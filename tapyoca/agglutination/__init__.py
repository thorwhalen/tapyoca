import requests
import re
import inspect
import importlib
import pkgutil

import sys
import os

pkg_folder = os.path.dirname(__file__)
mjoin = lambda *p: os.path.join(pkg_folder, *p)

