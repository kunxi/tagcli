#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='tagcli',
    version='0.2.0',
    description='A mutagen-based tag editor.',
    author='Kun Xi',
    author_email='kunxi@kunxi.org',
    url='https://github.com/kunxi/tagcli',
    py_modules=[
        'tagcli',
    ],
    include_package_data=True,
    install_requires=[
        'docopt',
        'mutagen'
    ],
    test_require=['pytest'],
    entry_points="""
    [console_scripts]
    tag= tagcli:main
    """,
    license="BSD",
    zip_safe=False,
    keywords='tagcli',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
)
