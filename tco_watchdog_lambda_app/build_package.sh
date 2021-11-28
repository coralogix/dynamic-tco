#!/bin/bash
FILE="${0}"
FILENAME=$(basename "${FILE}")
FOLDER=$(dirname "${FILE}")

rm deployment-package.zip
pip3 install --target "${FOLDER}/package" -r "${FOLDER}/requirements.txt"
cd "${FOLDER}/package" || exit 9
zip -r ../deployment-package.zip .
cd ..
zip -g deployment-package.zip ./*.py