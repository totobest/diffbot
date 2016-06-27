#!/usr/bin/env bash

set -e

version="v3"

. venv/bin/activate
pyinstaller -F -y bing-api.spec
pyinstaller -F -y diffbot-api.spec

cp settings.ini dist/settings.ini

rm -f dist/*.log
rm -f dist/*.csv
rm -f dist/.DS_Store

zip -r bing-diffbot-${version}.zip dist
git archive master -o bing-diffbot-${version}-src.zip
