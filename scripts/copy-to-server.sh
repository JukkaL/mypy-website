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
ssh mypy-lang.org "mkdir web || true"
scp *.html *.css mypy-lang.org:web/
ssh mypy-lang.org "sudo cp web/* /srv/www-mypy/"

echo "=== Done"
