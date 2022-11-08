#!/bin/sh
set -eu

echo "=== Building web site..."
python build.py

if [ ! -f out/index.html ]; then
    echo "Error: The out/ directory does not seem to contain generated files!"
    exit 1
fi

echo "=== Copying web site to mypy-lang.org..."
cd out
ssh mypy-lang.org "mkdir -p web/static"
scp -r *.html *.css static favicon.ico mypy-lang.org:web/
ssh mypy-lang.org "sudo cp -r web/* /srv/www-mypy/"

echo "=== Done"
