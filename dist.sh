#!/usr/bin/env bash

set -e

version="v6"

. venv/bin/activate
pyinstaller -F -y bing-api.spec
pyinstaller -F -y diffbot-api.spec

cp settings.ini dist/settings.ini

npm install markdown-pdf
node_modules/markdown-pdf/bin/markdown-pdf README.md -o dist/README.pdf

rm -f dist/*.log
rm -f dist/*.csv
rm -f dist/.DS_Store

zip -r bing-diffbot-${version}.zip dist
git archive master -o bing-diffbot-src-${version}.zip
