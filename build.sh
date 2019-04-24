#!/bin/bash
cd "$RECIPE_DIR"/.. || exit
$PYTHON setup.py install --single-version-externally-managed --record=record.txt
