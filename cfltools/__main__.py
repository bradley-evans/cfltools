import sys
import argparse

def parseArguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--getuniqueips',nargs=1)
    args = parser.parse_args()

    if args.getuniqueips:
        # Perform the following steps:
        #   (1) Get the unique IP addresses from <filename>
        #   (2) Export the unique IP addresses to a local text file (a report).
        #   (3) Export the unique IP addresses to a csv file.
        #   We include the frequency of each IP address' appearance.
        import cfltools.logparse.getuniqueip as getuniqueip
        for filename in args.getuniqueips:
            print('Getting unique ips from filename {}.'.format(filename))
            getuniqueip.run(filename)


def main():
    # Expermental code #
    # Don't judge me, I'm new to this. #
    print('in main')
    args = sys.argv[1:]
    print('argument count :: {}'.format(len(args)))
    for arg in args:
        print('passed argument :: {}'.format(arg))
    parseArguments(args)
