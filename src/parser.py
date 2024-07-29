from sys import exit

'''
How many fields are in the APF form

All fields' values will be stored in a list named 'lt' in the parse() function.
Each field's value can be found at index (n-1), where n = its ordinal position
in the APF's field list (see ../formOriginals/apfFields.csv)
'''
NUM_FIELDS = 109

'''
Reads and handles the values of the given record and outputs their validated values
as a list whose elements correspond to the fields in the APF form.

Params:
H = Headers from the csv file exported out of REDCap
R = The record we're currently parsing

Returns:
A list of length n, where n is the number of fields in the APF form.  The appropriate
value to fill each field in with will be at index (n-1).
'''
def parse(H: list, R: list) -> list:
    lt = [None] * NUM_FIELDS
    lt[15] = hmsTitle(H, R)
    pSearch(H, R, lt)
    print(lt)

    return lt

'''
Checks if the given column exists, then returns its value.  If the value was null,
returns an empty string ('').
'''
def getVal(H: list, R: list, colNm: str) -> str:
    try:
        return R[H.index(colNm)]
    except ValueError as e:
        exit('ERROR: The row \'{}\' does not exist in the REDCap export.'.format(colNm))

'''
Returns the HMS title from the given REDCap record.

The HMS title value lies in 1 of many fields in REDCap.  Because of the design of the
survey, we are guaranteed to only have a value in 1 of the fields, the rest of the fields
will be empty.

Caution: All fields could be empty (no title was selected).
'''
def hmsTitle(H: list, R: list) -> str:
    LABELS  = [
        'Select Harvard title:',
        'Full-time: Greater than 4 days at MGH',
        'Part-time 1-4 Days at MGH',
        'Less than 1 day at MGH'
    ]
    OTHER = [
        'Non-trainee title',
        'Other/Not Sure',
        'None'
    ]
    HOLDING = [
        'Assistant Professor, with holding title of Member of the Faculty',
        'Associate Professor, with holding title of Member of the Faculty',
        'Professor, with holding title of Member of the Faculty',
        'Assistant Professor, Part-time with holding title of Member of the Faculty',
        'Associate Professor, Part-time with holding title of Member of the Faculty',
        'Professor, Part-time with holding title of Member of the Faculty'
    ]

    match = ''

    # Find non-empty value
    for field in LABELS:
        match = getVal(H, R, field)
        if (match):
            break
    
    # Disregard 'other' responses
    if (match in OTHER):
        match = ''

    # Trim off holding appointment language
    if (match in HOLDING):
        match = match[0:-44]

    return match

# Sets value for fields regarding the Search Report
def pSearch(H: list, R: list, lt: list):
    TRAINEES = [
        'Research Fellow',
        'Clinical Fellow'
    ]

    search = getVal(H, R, 'Search Report')

    if (search == 'Not Required' or search == ''):
        lt[0] = 'No'
        lt[2] = 'Yes'
        if (lt[15] in TRAINEES):
            lt[3] = 'Trainee appointment'
        ''' TODO: Add search exception exclusive selection REDCap field
        else:
            lt[3] = getVal(H, R, 'Search Exception Reason')
        '''
    else:
        lt[0] = 'Yes'
        lt[2] = 'No'
        # TODO: lt[1] = getVal(H, R, 'Search Portal ID')