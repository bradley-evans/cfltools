import sys
import argparse

#

def flag_getuniqueips (filenames):
    import cfltools.logparse.getuniqueip as getuniqueip
    for filename in filenames:
        print('Getting unique ips from filename {}.'.format(filename))
        getuniqueip.run(filename)

def parseArguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--getuniqueips',nargs=1)
    args = parser.parse_args()

    if args.getuniqueips:
        flag_getuniqueips(args.getuniqueips)

def main():
    # Expermental code #
    # Don't judge me, I'm new to this. #
    print('in main')
    args = sys.argv[1:]
    print('argument count :: {}'.format(len(args)))
    for arg in args:
        print('passed argument :: {}'.format(arg))
    parseArguments(args)

if __name__ == '__main__':
    main()
