#!/usr/bin/env bash

echo "This script will run the tests defined in tests/"
echo "Before running the tests,"
echo "you need to create the '*.feature' files and '*steps.js'"
echo ""

npx bddgen \
    && npx playwright test \
    --ui \
    --project chromium

echo "--done--"