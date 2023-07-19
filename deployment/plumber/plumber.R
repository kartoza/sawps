# plumber.R

#* Echo back the input
#* @get /echo
function() {
  list(msg = paste0("Plumber is working!"))
}
