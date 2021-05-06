#!/bin/bash
set -e

# Requirements (Fedora)
# sudo dnf install python3-virtualenv

HERE=$(dirname "$(readlink --canonicalize "$BASH_SOURCE")")
cd "$HERE"

VERSION=$(git describe --tags --always)
echo "__version__ = \"$VERSION\"" > "$HERE/ard/version.py"

rm --force --recursive dist
mkdir --parents dist

rm --recursive --force dist/env
python3 -m venv --upgrade-deps dist/env
. dist/env/bin/activate
python -m pip install wheel

if [ "$1" == -e ]; then

    # Install editable
    python -m pip install --editable .

else
    # Build
    ./setup.py sdist bdist_wheel

    SDIST=dist/ard-$VERSION.tar.gz
    BDIST=dist/ard-$VERSION-py3-none-any.whl

    if [ "$1" == -s ]; then

        # Install sdist
        python -m pip install "$SDIST"

    elif [ "$1" == -b ]; then

        # Install bdist
        python -m pip install "$BDIST"

    elif [ "$1" == -p ]; then

        # Publish

        python -m pip install twine

        gpg --detach-sign --armor --yes "$SDIST"
        gpg --detach-sign --armor --yes "$BDIST"

        # Upload to PyPI
        twine upload \
            "$SDIST" \
            "$SDIST.asc" \
            "$BDIST" \
            "$BDIST.asc"

    fi
fi
