set -e
set -x

# R commands
echo '.libPaths( c( "'"$R_LIB_USER"'", .libPaths()) )' >> .Rprofile
echo 'options(repos=structure(c(CRAN="http://cran.rstudio.com")))' >> .Rprofile
R -q -e 'install.packages("lintr")'
R -q -e 'install.packages("formatR")'
