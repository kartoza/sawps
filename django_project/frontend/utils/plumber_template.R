# plumber.R

library(tidyverse)
library(tidygam)
library(mgcv)
library(ggpubr)

#* Echo back the input
#* @get /statistical/echo
function() {
  list(msg = paste0("Plumber is working!"))
}
