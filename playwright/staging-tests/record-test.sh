#!/usr/bin/env bash

if [ -z "$1" ]
then
  echo "Usage: $0 TESTNAME"
  echo "e.g. $0 mytest"
  echo "will write a new test to tests/mytest.spec.ts"
  echo "Do not use spaces in your test name."
  echo ""
  echo "After recording your test, close the test browser."
  echo "You can then run your test by doing:"
  echo "npx playwright test tests/mytest.spec.py"
  exit
else
  echo "Recording test to tests\$1"
fi

if [ -w "tests/${1}.spec.ts" ]; then
   # File exists and write permission granted to user
   # show prompt
   echo "File tests/${1}.spec.ts exists. Overwrite? y/n"
   read ANSWER
   case $ANSWER in 
       [yY] ) echo "Writing recorded test to tests/${1}.spec.ts" ;;
       [nN] ) echo "Cancelled."; exit ;;
   esac
fi
TESTNAME=$1

npx playwright \
  codegen \
  --load-storage=tests/.auth/sawps-auth.json \
  -o tests/$TESTNAME.spec.ts \
  http://sawps.sta.do.kartoza.com

echo "Test recording completed."
echo "You can then run your test by doing:"
echo "npx playwright test tests/$1.spec.ts"
