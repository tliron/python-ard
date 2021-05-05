#!/bin/bash
set -e

# Requirements (Fedora)
# sudo dnf install python3-virtualenv

HERE=$(dirname "$(readlink --canonicalize "$BASH_SOURCE")")
cd "$HERE"

VERSION=$(git describe --tags --always)
echo -n "$VERSION" > VERSION
#echo "__version__ = '$VERSION'" > ard/__init__.py

rm --force --recursive dist
mkdir --parents dist

rm --recursive --force dist/env
python3 -m venv --upgrade-deps dist/env
. dist/env/bin/activate
python -m pip install wheel

if [ "$1" == -p ]; then

    # Publish

    SDIST=dist/ard-$VERSION.tar.gz
    BDIST=dist/ard-$VERSION-py3-none-any.whl

    python -m pip install twine

    ./setup.py sdist bdist_wheel

    gpg --detach-sign --armor --yes "$SDIST"
    gpg --detach-sign --armor --yes "$BDIST"

    # Upload to PyPI
    twine upload \
        "$SDIST" \
        "$SDIST.asc" \
        "$BDIST" \
        "$BDIST.asc"

else

    # Install

    python -m pip install .

fi
