__author__ = 'hamdiahmadi'

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("PalindromicSubstringsDiv2_cython.pyx")
)