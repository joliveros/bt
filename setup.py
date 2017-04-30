from setuptools import find_packages, setup, Extension
import codecs
import os
import re
from pip.req import parse_requirements
from pip.download import PipSession
from os.path import realpath


def get_reqs_from_file(file):
    file_path = realpath(file)

    # parse_requirements() returns generator of pip.req.InstallRequirement objects
    install_reqs = parse_requirements(file_path, session=PipSession)

    # reqs is a list of requirement
    # e.g. ['django==1.5.1', 'mezzanine==1.4.6']
    return [str(ir.req) for ir in install_reqs]


def local_file(filename):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), filename), 'r', 'utf-8'
    )

version = re.search(
    "^__version__ = \((\d+), (\d+), (\d+)\)",
    local_file(os.path.join('bt', '__init__.py')).read(),
    re.MULTILINE
).groups()

try:
    from Cython.Build import cythonize
except ImportError:
    use_cython = False
else:
    use_cython = True

ext_modules = []

if use_cython:
    ext_modules = cythonize('bt/core.py')
else:
    ext_modules = [
        Extension('bt.core', ['bt/core.c'])
    ]

setup(
    name="bt",
    version='.'.join(version),
    author='Philippe Morissette',
    author_email='morissette.philippe@gmail.com',
    description='A flexible backtesting framework for Python',
    keywords='python finance quant backtesting strategies',
    url='https://github.com/pmorissette/bt',
    install_requires=[
        'ffn',
        'pyprind>=2.10'
    ],
    packages=['bt'],
    long_description=local_file('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python'
    ],
    ext_modules=ext_modules
)
