#!/usr/bin/env python
# coding: utf-8

import os.path
from setuptools import setup, find_packages
from dots import VERSION

SRCDIR = os.path.realpath(os.path.dirname(__file__))
with open(os.path.join(SRCDIR, 'README.md')) as ifile:
    README = ifile.read()
with open(os.path.join(SRCDIR, 'requirements.txt')) as ifile:
    REQUIREMENTS = ifile.read().strip().splitlines()

setup(
    name='dots',
    version=VERSION,
    description='Configuration files management tool',
    long_description=README,
    author='Mathieu Deous',
    author_email='mattoufootu+py@gmail.com',
    url='https://github.com/mattoufoutu/dots',
    license='BSD',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': ['dots = dots.cli:main']
    }
)
