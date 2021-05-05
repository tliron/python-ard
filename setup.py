#!/usr/bin/env python3

import os.path, setuptools

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    version = f.read()

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
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
