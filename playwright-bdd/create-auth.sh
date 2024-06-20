#!/usr/bin/env bash

echo "This script will run the tests defined in tests/"
echo "Before running the tests,"
echo "you need to create the '*.feature' files and '*steps.js'"
echo ""

source base-url.sh

npx bddgen \
    && npx playwright \
    codegen \
	--target playwright-test \
	--save-storage=auth.json \
	-o steps/deleteme.spec.ts \
	$BASE_URL

rm steps/deleteme.spec.ts

echo "--done--"