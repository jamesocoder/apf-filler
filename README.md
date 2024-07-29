# Academic Profile Form Filler

On 2024-07-01, the Harvard Medical School's Office for Faculty Affairs mandated the use of a new form that forced an unreasonable amount of duplicative data entry upon its affiliate organizations.  For every new hire, they would now have to enter things like full name multiple times into different systems.

To fix this issue, an executable script will be devised that will take in data from our initial point of entry (REDCap, exported as a csv) and enter it into the form.  To do so, we will use Adobe's PDF Form data import feature, which allows a user to import an XML file to fill its fields.

There is an opportunity for further automation, more script can be written to utilize [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/), a purchasable command-line tool that automates importing data and then outputting a new, filled PDF.

## Obtaining a Template XML File

To obtain an XML file that lists all of the fields on the form, first fill every field with dummy data.  Then, using Adobe Acrobat, Menu->Form Options->Export Data...

Make sure to choose XML as the file type.

## Setup

This was written with Python 3.12.4

Make sure to install pip with your Python installation, then use `pip install pyinstaller`.  This package assists with turning the script into an .exe file.

## How to build

The .exe file can be built with `python -m PyInstaller --onefile ./src/main.py`

## How to run

The program can either be run without Python installed after it is built into an .exe or directly from the python file with Python installed.  To run it directly from the script, use `python ./src/main.py`.