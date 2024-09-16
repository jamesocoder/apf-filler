from sys import exit
from datetime import date

'''
How many fields are in the APF form + 1

The last element of the list will house the Record ID to name the XML file with.

All field values will be stored in a list named 'lt' in the parse() function.
Each field's value can be found at index (n-1), where n = its ordinal position
in the APF's field list (see ../formOriginals/apfFields.csv)
'''
NUM_FIELDS = 109 + 1

INSTITUTION = 'MGH'
TRAINEE_TITLES = [
    'Research Fellow',
    'Clinical Fellow'
]

def clinFellowGradDate(H: list, R: list) -> str:
    val = getVal(H, R, 'Medical School Graduation Date')
    if (len(val)):
        return date.fromisoformat(val).strftime('%m/%Y')
    else:
        val = getVal(H, R, 'Medical School Attendance Dates')
        if (len(val)):
            try:
                # Extract graduation date from '____ - ____'
                val = val[val.index(' - ') + 3:]
                return checkGradDate(val)
            except ValueError as e:
                raise e

def checkGradDate(val: str) -> str:
    slashCnt = len(val) - len(val.replace('/', ''))
    match slashCnt:
        case 0:
            # val looks like 'text'
            # Assume new hire entered a year
            return '6/' + val
        case 1:
            # val likely looks like 'text1/text2'
            # Check if text1 is a month or a year
            leftNum = int(val[:val.index('/')])
            if (leftNum < 13):
                # Assume val is 'month/year'
                return val
            else:
                # Assume val is 'year/month'
                return '{}/{}'.format(
                    val[val.index('/') + 1:],
                    leftNum
                )
        case 2:
            # val likely looks like 'text1/text2/text3'
            # Check if text1 is a month or day
            slash01Index = val.index('/')
            text1 = int(val[:slash01Index])
            if (text1 < 13):
                # Assume date is in month/day/year format
                return '{}{}'.format(
                    text1,
                    val[val.index('/', slash01Index + 1):]
                )
            else:
                # Assume date is in day/month/year format
                return val[slash01Index + 1:]



def parseClinFellow(type: int, preparer: str, H: list, R: list) -> list:
    lt = [None] * NUM_FIELDS

    if (type == 1):
        lt[14] = 'Clinical Fellow'
        lt[9] = getVal(H, R, 'Medical Degree Abbreviation')
        lt[19] = date(date.today().year, 7, 1).isoformat()
    elif(type == 2):
        lt[14] = 'Resident'
        lt[9] = getVal(H, R, 'Degree Abbreviation')

    lt[0] = "No"
    lt[2] = "Yes"
    lt[3] = "Trainee appointment"
    lt[4:8] = [
        getVal(H, R, 'Last Name'),
        getVal(H, R, 'First Name'),
        getVal(H, R, 'Middle Name'),
        date.fromisoformat(
            getVal(H, R, 'Date of Birth')
        ).strftime('%m/%d/%Y')
    ]
    lt[12] = INSTITUTION
    lt[15] = 'Clinical Fellow'
    lt[20] = date(date.today().year + 1, 6, 30).isoformat()
    lt[22] = 'Affiliate'
    lt[26] = INSTITUTION + ' (Boston, MA)'
    lt[30] = '5.0'
    lt[34] = lt[14]
    lt[38] = 'Appointment required for library access and participation in ' + \
        'certain programs and/or grant applications.'
    lt[39] = 'No'
    lt[41:45] = [
        'Yes', 'Yes', 'Yes',
        getVal(H, R, 'Will you need a VISA?')
    ]
    if (lt[44] == 'Yes'):
        lt[45:50] = [
            getVal(H, R, 'Current Visa Type'),
            INSTITUTION,
            getVal(H, R, 'Current Visa Start Date'),
            getVal(H, R, 'Current Visa End Date'),
            getVal(H, R, 'Current Visa ID Number')
        ]
    try:
        lt[58] = clinFellowGradDate(H, R)
    except ValueError as e:
        exit(
            '{} {} '.format(lt[5], lt[4]) + 'is either missing a graduation ' + \
            'date or has a malformatted one.  Check that the medical school ' + \
            'attendance dates are in \"m/d/yyyy - m/d/yyyy\" format.'
        )
    lt[59:62] = [
        lt[9],
        'Medicine',
        getVal(H, R, 'Medical School Name')
    ]
    lt[98:102] = [
        str(date.today().year) + '-present',
        lt[14],
        'Medicine',
        INSTITUTION
    ]
    lt[107:109] = [
        preparer,
        date.today().isoformat()
    ]
    lt[-1] = getVal(H, R, 'Record ID')

    return lt

'''
Reads and handles the values of the given record and outputs their validated values
as a list whose elements correspond to the fields in the APF form.

Params:
H = Headers from the csv file exported out of REDCap
R = The record we're currently parsing

Returns:
A list of length n, where n is the number of fields in the APF form.  The appropriate
value to fill each field in with will be at index (n-1).

Notes:
To avoid having to create lookup tables for the values corresponding to each REDCap
field's choice IDs, this script will require that the "labels" version of the data
be exported from REDCap instead of the "raw" version.
'''
def parse(preparer: str, H: list, R: list) -> list:
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

    lt[58:62] = [
        degreeDate(H, R, 'Date Completed (1)'),
        getVal(H, R, 'Degree (1)'),
        getVal(H, R, 'Major/Field of Study (1)'),
        getVal(H, R, 'Name of Institution where Medical or Doctoral degree was earned'),
    ]
    if (getVal(H, R, 'Degree (2)')):
        lt[62:66] = [
            degreeDate(H, R, 'Date Completed (2)'),
            getVal(H, R, 'Degree (2)'),
            getVal(H, R, 'Major/Field of Study (2)'),
            getVal(H, R, 'Name of Institution (2)')
        ]

    lt[98:102] = [
        str(date.fromisoformat(lt[19]).year) + '-present',
        lt[14],
        'Medicine ({})'.format(getDivision(H, R)),
        INSTITUTION
    ]

    lt[106] = getVal(H, R, 'Project Description')

    lt[107:109] = [
        preparer,
        date.today().isoformat()
    ]

    lt[-1] = getVal(H, R, 'Record ID')

    return lt

'''
Checks if the given column exists, then returns its value.  If the value was null,
returns an empty string ('').

Raises:
If the column name can't be found in the data, raises an error.
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
        match = match[0:-45]

    return match

# Sets value for fields regarding the Search Report
def pSearch(H: list, R: list, lt: list):
    search = getVal(H, R, 'Search Report')

    if (search == 'Not Required' or search == ''):
        lt[0] = 'No'
        lt[2] = 'Yes'
        if (lt[15] in TRAINEE_TITLES):
            lt[3] = 'Trainee appointment'
        else:
            lt[3] = getVal(H, R, 'Search Exception Reason')
    else:
        lt[0] = 'Yes'
        lt[2] = 'No'
        lt[1] = getVal(H, R, 'Search Portal ID')

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
        lt[47:50] = [
           getVal(H, R, 'Visa Start Date'),
           getVal(H, R, 'Visa End Date'),
           getVal(H, R, 'Visa ID Number')
        ]
    else:
        lt[44] = 'No'

def handleFacultySection(H: list, R: list, lt: list):
    if (lt[15] not in TRAINEE_TITLES):
       lt[55:58] = [
           'No',
           'N/A',
           'Requirement will be met with activity in the following areas: ' + 
           'teaching of students, residents, fellows, and postdocs; clinical ' +
           'and/or lab supervision, peer teaching, local presentations, ' +
           'mentoring, and/or educational administration.'
       ]

# The form's degree date fields must be in mm/yyyy format
def degreeDate(H: list, R: list, colNm: str) -> str:
    return date.fromisoformat(
        getVal(H, R, colNm)
    ).strftime('%m/%Y')

# Ampersands must be escaped in XML files
def getDivision(H: list, R: list) -> str:
    out = getVal(H, R, 'Division, Research Center or Research Unit')
    return out.replace('&', "&amp;")