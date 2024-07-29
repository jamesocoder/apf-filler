import sys, csv

# TODO: Look into https://docs.python.org/3/howto/argparse.html instead of sys.argv
def main():
    with open(sys.argv[1]) as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                print(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(sys.argv[1], reader.line_num, e))
        

if __name__ == '__main__':
    main()