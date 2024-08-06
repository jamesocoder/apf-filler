::Script Version 1.0
::TODO: pdftk's fill_form is encountering an Unhandled Java Exception

::Parameters:
::%1 = REDCap output, labelled version
::%2 = User's full name
::%3 = REDCap Record ID
::%4 = Name to save filled APF form as

apf-filler.exe %1.csv %2

"C:\Program Files (x86)\PDFtk Server\bin\pdftk.exe" apf-unencrypted.pdf fill_form %3.xml output %4.pdf

del %3.xml /F

::pause

::exit
