with import <nixpkgs> { };

let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell rec {
  name = "R";
  buildInputs = [
    rstudio
    rPackages.tidyverse
    # The rest of these should probably not
    # be needed since tidyverse would pull them in
    # anyway
    curl
    fontconfig
    fribidi
    harfbuzz
    libtiff
    pkg-config
    rPackages.googledrive
    rPackages.googlesheets4
    rPackages.httr
    rPackages.openssl
    rPackages.ragg
    rPackages.rvest
    rPackages.systemfonts
    rPackages.xml2
    rstudio
    xml2
  ];

}

