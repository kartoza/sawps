#!/usr/bin/env bash

echo "This script will discover the path to your playwright install"
echo "If you are not in  a NixOS environment and it is not installed,"
echo "it will try to install it."
echo ""
echo "At the end of calling this script , you should have a PLAYWRIGHT"
echo ""

# Are we on nixos or a distro with Nix installed for packages
# Y
  # Are we in direnv?
  # Y: should all be set up
  # N: run nix-shell
#N
 # Are we in a deb based distro?
 # Are we in an rpm based distro?
 # Are we on macOS?
 # Are we in windows?

HAS_PLAYWRIGHT=$(which playwright | grep -v "which: no" | wc -l)
PLAYWRIGHT="playwright"
if [ $HAS_PLAYWRIGHT -eq 0 ]; then
  PLAYWRIGHT="npx playwright"
  
  # check if it is a deb based distro
  USES_APT=$(which apt | grep -w "apt" | wc -l)
  NPM="npm"

  if [ $USES_APT -eq 1 ]; then
    PLAYWRIGHT_INSTALL=$($NPM ls --depth 1 playwright | grep -w "@playwright/test" | wc -l)

    if [ $PLAYWRIGHT_INSTALL -eq 0 ]; then
      $NPM install
      $PLAYWRIGHT install --with-deps chromium
    fi

  fi

fi

echo "Done."
echo ""
