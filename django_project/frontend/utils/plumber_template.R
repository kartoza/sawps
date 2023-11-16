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


#* Echo back the input
#* @get /statistical/test
function() {
  metadata <- list(species='test',generated_on=Sys.time())
  time_start<-Sys.time()
  metadata['total_execution_time'] <- Sys.time() - time_start
  list(metadata=metadata)
}
