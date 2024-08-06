:: Shortcut to Academic Profile Form Filler
:: Version 1.0
:: Save this file to cmd's default directory (C:\Users\[Username])
:: Can be run from cmd's default directory with command: apf
:: Expects the APF REDCap report to be downloaded to the APF directory as apf.csv

cd Desktop/APF

apf-filler.exe apf.csv "James Ouk"

:: Assumes Adobe Acrobat is the default program for PDFs
start APF_Original.pdf

cd ../..