# Academic Profile Form Filler

On 2024-07-01, the Harvard Medical School's Office for Faculty Affairs mandated the use of a new form that forced an unreasonable amount of duplicative data entry upon its affiliate organizations.  For every new hire, they would now have to enter things like full name multiple times into different systems.

To fix this issue, an executable script will be devised that will take in data from our initial point of entry (REDCap, exported as a csv) and enter it into the form.  To do so, we will use Adobe's PDF Form data import feature, which allows a user to import an XML file to fill its fields.

## Obtaining a Template XML File

To obtain an XML file that lists all of the fields on the form, first fill every field with dummy data.  Then, using Adobe Acrobat, Menu->Form Options->Export Data...

Make sure to choose XML as the file type.

## Setup

This was written with Python 3.12.4

Make sure to install pip with your Python installation, then use `pip install pyinstaller`.  This package assists with turning the script into an .exe file.

## How to build

The .exe file can be built with `python -m PyInstaller --onefile ./src/main.py`

## How to run

To run after compiling into an executable:
- With a terminal, run the executable and supply it with the relative path to [label.csv](/dataSamples/label.csv) and your name as command-line arguments

To run directly with Python installed:
- In a terminal with the project root opened, `python ./src/main.py ./dataSamples/label.csv [your_name]`

## Further Automation with PDFTK

There is an opportunity for another CLI script to be written to utilize [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/), a purchasable command-line tool that automates importing data and then outputting a new, filled PDF.

The original PDF may need to be unencrypted with [qpdf](https://github.com/qpdf/qpdf) first using this command:

`qpdf.exe --decrypt [encrypted.pdf] [outputName.pdf]`

- See [gitlab](https://gitlab.com/pdftk-java/pdftk/-/issues/87) for more context.

Going further with this eventually led me to an `Unhandled Java Exception: Bookmark is not the root element` from pdftk's `fill_form` command.  I then found [this discussion](https://stackoverflow.com/questions/36613976/pdftk-throws-a-java-exception-when-attempting-to-use-fill-form-function), which leads me to suspect the XML isn't well-formed enough for pdftk yet.

The toolchain without pdftk automation works fine.  The user can use it to create an XML file that can be manually imported into the form using Adobe Acrobat.  While not ideal, the program is in a usable state.  Management is not supportive of further developing this project, so I will have to stop here.