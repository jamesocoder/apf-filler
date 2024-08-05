from csv import reader, Error as csvErr
from sys import argv, exit
from exporter import toXml as inSummary
from parser import parse as discombobulate

# TODO: Look into https://docs.python.org/3/howto/argparse.html instead of sys.argv
'''
To avoid having to create lookup tables for the values corresponding to each REDCap's
field's choices' IDs, this script will require that the "labels" version of the data
be exported instead of the "raw" version.
'''
def main():
    with open(argv[1]) as f:
        csv = reader(f)
        try:
            headers = next(csv)
            for row in csv:
                '''
                Each new hire record will be parsed into 'row' as a list
                We can use the column names in 'headers' to find the associative
                values in 'row' and then output them to an XML file

                /watch?v=B62ACxuq8Pw
                '''
                inSummary(
                    discombobulate(
                        headers,
                        row,
                        argv[2]
                    )
                )
        except csvErr as e:
            exit('file {}, line {}: {}'.format(argv[1], reader.line_num, e))
        

if __name__ == '__main__':
    main()