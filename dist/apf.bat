:: Shortcut to Academic Profile Form Filler
:: Version 1.1
:: Save this file to cmd's default directory (C:\Users\[Username])
:: Script can then be run from cmd's default directory with command: apf [APF_Program_Dir] [Full Name]
:: Can remove need for parameters by hard-coding program path and user's name in instead

:: Expects the APF REDCap report to be downloaded to the APF directory as apf.csv

:: Open APF program directory (1st CLI parameter)
cd %1

:: Execute XML creation with user's name (2nd CLI parameter)
:: Also receives Null, fellow, or resident (3rd CLI parameter).  Script callers can ignore the 3rd parameter to supply a Null.
apf-filler.exe apf.csv %2 %3

:: Assumes Adobe Acrobat is the default program for PDFs
:: Open the APF to allow the user to import the XML into it
start APF_Original.pdf

cd ../..
