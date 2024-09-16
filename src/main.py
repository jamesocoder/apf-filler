from csv import reader, Error as csvErr
from sys import argv, exit
from exporter import toXml as inSummary
from parser import parse as discombobulate, parseClinFellow as discombobulateTrainee

'''
Params:
argv3 = null or 1 if processing Clinical Fellows, else 2 if processing Residents

TODO: Look into https://docs.python.org/3/howto/argparse.html instead of sys.argv
'''
def main():
    match len(argv):
        case 4:
            try:
                cFellow = int(argv[3])
            except Exception as e:
                exit('apf-filler expects the 3rd argument to be either 1 or 2.  Review the instructions.')
            
            if (cFellow == 1 or cFellow == 2):
                holmes(cFellow)
            else:
                exit('An invalid 3rd argument value was given: {}'.format(argv[3]))
        case 3:
            holmes()
        case _:
            exit('apf-filler expects at least 2 arguments.  Review the instructions.')

'''
Handles opening the REDCap CSV file and passing it to helper functions for processing.

Params:
argv1 = Name of csv file from REDCap
clinFellowType = Number representing what type of clinical trainee we're processing, if any
argv2 = User's full name
'''
def holmes(clinFellowType = 0):
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