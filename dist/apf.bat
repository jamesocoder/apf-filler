::Script Version 1.0
::TODO: pdftk manipulation is blocked by some protection on the APF form.
::Forms suggest using qpdf to remove this protection.

::Parameters:
::%1 = REDCap output, labelled version
::%2 = User's full name
::%3 = REDCap Record ID
::%4 = Name to save filled APF form as

apf-filler.exe %1.csv %2

"C:\Program Files (x86)\PDFtk Server\bin\pdftk.exe" APF_Original.pdf fill_form %3.xml output %4.pdf

del %3.xml /F

::pause

::exit