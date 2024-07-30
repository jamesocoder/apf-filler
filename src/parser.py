from sys import exit
from datetime import date

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
def parse(H: list, R: list, preparer: str) -> list:
    '''
    How many fields are in the APF form

    All fields' values will be stored in a list named 'lt' in the parse() function.
    Each field's value can be found at index (n-1), where n = its ordinal position
    in the APF's field list (see ../formOriginals/apfFields.csv)
    '''
    NUM_FIELDS = 109
    INSTITUTION = 'MGH'

    lt = [None] * NUM_FIELDS

    lt[15] = hmsTitle(H, R)

    pSearch(H, R, lt)

    lt[4:8] = [
        getVal(H, R, 'Candidate First Name'),
        getVal(H, R, 'Candidate Middle Name'),
        getVal(H, R, 'Candidate Last Name '),
        getVal(H, R, 'Date of birth')
    ]

    lt[9:11] = [
        getVal(H, R, 'Degree (1)'),
        getVal(H, R, 'Degree (2)')
    ]

    lt[12] = INSTITUTION
    # TODO: lt[14] = mghTitle(H, R)
    lt[16:18] = ['Medicine', INSTITUTION]
    # TODO: lt[18] = timeCommitment(H, R)
    lt[19] = getVal(H, R, 'Requested Start Date')
    # TODO: lt[20] = endDate()
    lt[21] = getVal(H, R, 'HMS Faculty Mentor (full name)')

    lt[22] = 'Affiliate'
    lt[26] = INSTITUTION + ' (Boston, MA)'
    lt[30] = getVal(H, R, 'Expected Days at location')
    lt[34] = lt[14]

    lt[38] = 'Appointment required for library access and participation in ' + \
        'certain programs and/or grant applications.'
    
    lt[39] = 'No'
    lt[41] = 'Yes'
    # TODO: lt[42] = clinicalCreds(H, R)
    lt[43] = 'Yes'

    # TODO: handleVisa(H, R, lt)

    # TODO: if (faculty): handleFacultySection(H, R, lt)

    # TODO: Add degree major fields
    lt[58:66] = [
        getVal(H, R, 'Date Completed (1)'),
        getVal(H, R, 'Degree (1)'),
        '',
        getVal(H, R, 'Name of Institution where Medical or Doctoral degree was earned'),
        getVal(H, R, 'Date Completed (2)'),
        getVal(H, R, 'Degree (2)'),
        '',
        getVal(H, R, 'Name of Institution (2)')
    ]

    lt[98:102] = [
        str(date.fromisoformat(lt[19]).year) + '-present',
        lt[14],
        'Medicine ({})'.format(getVal(H, R, 'Division, Research Center or Research Unit')),
        INSTITUTION
    ]

    # TODO: lt[106] = getVal(H, R, 'Work/Project Description')

    lt[107:109] = [
        preparer,
        date.today().strftime('%m/%d/%Y')
    ]

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