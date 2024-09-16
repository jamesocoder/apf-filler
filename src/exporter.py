'''
Outputs the parsed data into an XML file that the PDF form's import function will
accept.

Parameters:
vals = The list output by parser.parse.  Expects the last field in this list to contain
the REDCap Record ID.  This is intended to make it easier to slot this output into
our database's existing automation.
'''
def toXml(vals: list):
    with open(vals[-1] + '.xml', 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n\n')
        f.write('<fields xmlns:xfdf="http://ns.adobe.com/xfdf-transition/">\n')
        for i, v in enumerate(vals):
            if (v and i != (len(vals) - 1)):
                f.write('    <field xfdf:original="{:03d}">{}</field>\n'.format(
                    i + 1,
                    v
                ))
        f.write('</fields>')