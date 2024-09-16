from csv import reader, Error as csvErr
from sys import argv, exit
from exporter import toXml as inSummary
from parser import parse as discombobulate, parseClinFellow as discombobulateTrainee

def main():
    '''
    Params:
    argv1 = Name of csv file from REDCap
    argv2 = User's full name
    argv3 = null, 'fellow', or 'resident'

    TODO: Look into https://docs.python.org/3/howto/argparse.html instead of sys.argv
    '''
    match len(argv):
        case 4:
            if (argv[3] == 'fellow'):
                holmes(1)
            elif (argv[3] == 'resident'):
                holmes(2)
            else:
                exit('An invalid 3rd launch argument was given: {}'.format(argv[3]))
        case 3:
            holmes()
        case _:
            exit('apf-filler expects at least 2 arguments.  Review the instructions.')

def holmes(clinFellowType = 0):
    '''
    Handles opening the REDCap CSV file and passing it to helper functions for processing.

    Params:
    clinFellowType = Number representing what type of clinical trainee we're processing, if any;
        0 for rolling intake form
        1 for clinical fellow
        2 for resident
    '''
    with open(argv[1]) as f:
        csv = reader(f)
        try:
            headers = next(csv)
            if (clinFellowType == 0):
                for row in csv:
                    '''
                    Each new hire record will be parsed into 'row' as a list
                    We can use the column names in 'headers' to find the associative
                    values in 'row' and then output them to an XML file

                    /watch?v=B62ACxuq8Pw
                    '''
                    inSummary(
                        discombobulate(
                            argv[2],
                            headers,
                            row
                        )
                    )
            else:
                for row in csv:
                    inSummary(
                        discombobulateTrainee(
                            clinFellowType,
                            argv[2],
                            headers,
                            row
                        )
                    )
        except csvErr as e:
            exit('file {}, line {}: {}'.format(argv[1], reader.line_num, e))

if __name__ == '__main__':
    main()