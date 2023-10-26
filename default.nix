with import <nixpkgs> { };

let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell rec {
  name = "R";
  buildInputs = [
    curl 
    fontconfig 
    fribidi 
    harfbuzz 
    libtiff 
    pkg-config 
    rstudio
    rPackages.googledrive 
    rPackages.googlesheets4 
    rPackages.httr 
    rPackages.openssl 
    rPackages.ragg 
    rPackages.rvest
    rPackages.systemfonts 
    rPackages.tidyverse
    rPackages.xml2 
    rstudio 
    xml2 
  ];

}

