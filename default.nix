with import <nixpkgs> { };

let
  pkgs = import <nixpkgs> {};
  RStudio-with-my-packages = rstudioWrapper.override{
      packages = with rPackages; [ tidyverse snakecase ]; };
in pkgs.mkShell rec {
  name = "R";
  buildInputs = [
    RStudio-with-my-packages
  ];

}

