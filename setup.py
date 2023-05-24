#!/usr/bin/env python3

import pathlib, setuptools

here = pathlib.Path(__file__).parents[0]

with open(here / 'ard' / 'version.py') as f:
  globals_ = {}
  exec(f.read(), globals_)
  version = globals_['__version__']

with open(here / 'README.md') as f:
  readme = f.read()

setuptools.setup(
  name='ard',
  version=version,
  description='Agnostic Raw Data for Python',
  long_description=readme,
  long_description_content_type='text/markdown',
  license='Apache License 2.0',
  author='Tal Liron',
  author_email='tal.liron@gmail.com',
  url='https://github.com/tliron/python-ard',
  download_url='https://github.com/tliron/python-ard/releases',
  classifiers=(
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License'),

  packages=('ard',),
  scripts=('ardconv',),
  install_requires=('ruamel.yaml', 'cbor2'))
