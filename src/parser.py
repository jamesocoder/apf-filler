from sys import exit
from datetime import date

INSTITUTION = 'MGH'

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
    How many fields are in the APF form + 1

    The last element of the list will house the Record ID to name the XML file with.

    All fields' values will be stored in a list named 'lt' in the parse() function.
    Each field's value can be found at index (n-1), where n = its ordinal position
    in the APF's field list (see ../formOriginals/apfFields.csv)
    '''
    NUM_FIELDS = 109 + 1
    lt = [None] * NUM_FIELDS

    lt[15] = hmsTitle(H, R)

    pSearch(H, R, lt)

    lt[4:8] = [
        getVal(H, R, 'Candidate Last Name '),
        getVal(H, R, 'Candidate First Name'),
        getVal(H, R, 'Candidate Middle Name'),
        date.fromisoformat(
            getVal(H, R, 'Date of birth')
        ).strftime('%m/%d/%Y')
    ]

    lt[9:11] = [
        getVal(H, R, 'Degree (1)'),
        getVal(H, R, 'Degree (2)')
    ]

    lt[12] = INSTITUTION
    lt[14] = mghTitle(H, R)
    lt[16:18] = ['Medicine', INSTITUTION]
    lt[18] = timeCommitment(H, R)

    lt[19] = getVal(H, R, 'Requested Start Date')
    lt[20] = calculateEndDate(lt)

    lt[21] = getVal(H, R, 'HMS Faculty Mentor (full name)')

    lt[22] = 'Affiliate'
    lt[26] = INSTITUTION + ' (Boston, MA)'
    lt[30] = getVal(H, R, 'Expected Days at location')
    lt[34] = lt[14]

    lt[38] = 'Appointment required for library access and participation in ' + \
        'certain programs and/or grant applications.'
    
    lt[39] = 'No'
    lt[41] = 'Yes'
    lt[42] = clinicalCredentials(H, R)
    lt[43] = 'Yes'

    handleVisa(H, R, lt)

    handleFacultySection(H, R, lt)

    # TODO: Add degree major fields
    lt[58:66] = [
        degreeDate(H, R, 'Date Completed (1)'),
        getVal(H, R, 'Degree (1)'),
        '',
        getVal(H, R, 'Name of Institution where Medical or Doctoral degree was earned'),
        degreeDate(H, R, 'Date Completed (2)'),
        getVal(H, R, 'Degree (2)'),
        '',
        getVal(H, R, 'Name of Institution (2)')
    ]

    lt[98:102] = [
        str(date.fromisoformat(lt[19]).year) + '-present',
        lt[14],
        'Medicine ({})'.format(getDivision(H, R)),
        INSTITUTION
    ]

    # TODO: lt[106] = getVal(H, R, 'Work/Project Description')

    lt[107:109] = [
        preparer,
        date.today().isoformat()
    ]

    lt[-1] = getVal(H, R, 'Record ID')

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

CAUTION: All fields could be empty (no title was selected).  It is up to the user to
address this possiblity before running the script.
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
        ''' TODO: Add search exception radio selection REDCap field
        else:
            lt[3] = getVal(H, R, 'Search Exception Reason')
        '''
    else:
        lt[0] = 'Yes'
        lt[2] = 'No'
        # TODO: lt[1] = getVal(H, R, 'Search Portal ID')

def mghTitle(H: list, R: list) -> str:
    if (getVal(H, R, 'Appointment Type') == 'Clinical'):
        return getVal(H, R, 'MGH Clinical Title')
    else:
        return getVal(H, R, 'MGH Non-Clinical Title ')

def timeCommitment(H: list, R: list) -> str:
    response = getVal(H, R,
        'How many days per week on average will the candidate be at MGH?'
    )
    if (response == 'Greater than or equal to 4 days'):
        return 'Full-time (works at least 4 days per week at HMS, ' + \
            'HSDM or a primary affiliate of HMS)'
    else:
        return 'Part-time (works at least 1, but less than 4, days ' + \
            'per week at HMS, HSDM or a primary affiliate of HMS)'

def calculateEndDate(lt: list) -> str:
    HOLDING = [
        'Assistant Professor',
        'Assistant Professor, Part-time',
        'Associate Professor',
        'Associate Professor, Part-time',
        'Professor',
        'Professor, Part-time'
    ]
    startDate = date.fromisoformat(lt[19])
    if (lt[15] in HOLDING):
        # End date is startDate + 1 year
        return date(startDate.year + 1, startDate.month, startDate.day).isoformat()
    else:
        # End date is 6/30 of next year
        return date(startDate.year + 1, 6, 30).isoformat()
    
def clinicalCredentials(H: list, R: list) -> str:
    return 'Yes' if (getVal(H, R, 'Appointment Type') == 'Clinical') else 'N/A'

def handleVisa(H: list, R: list, lt: list):
    if (getVal(H, R, 'Citizenship/Visa Status') == 'Visa Required'):
        lt[44] = 'Yes'
        vType = getVal(H, R, 'Visa Type')
        vOther = getVal(H, R, 'Please specify other Visa type  ')
        if (vType != ''):
            lt[45] = vType if (vOther == '') else vOther
        lt[46] = INSTITUTION
        # TODO: lt[47:50] = [
        #    getVal(H, R, 'Visa Start Date'),
        #    getVal(H, R, 'Visa End Date'),
        #    getVal(H, R, 'Visa ID Number')
        #]
    else:
        lt[44] = 'No'

def handleFacultySection(H: list, R: list, lt: list):
    TRAINEES = [
        'Research Fellow',
        'Clinical Fellow'
    ]

    # TODO: if (lt[15] not in TRAINEES):
    #    lt[55:58] = [
    #        'No',
    #        'N/A',
    #        getVal(H, R, 'Anticipated Teaching Activities')
    #    ]

# The form's degree date fields must be in mm/yyyy format
def degreeDate(H: list, R: list, colNm: str) -> str:
    return date.fromisoformat(
        getVal(H, R, colNm)
    ).strftime('%m/%Y')

# Ampersands must be escaped in XML files
def getDivision(H: list, R: list) -> str:
    out = getVal(H, R, 'Division, Research Center or Research Unit')
    return out.replace('&', "&amp;")