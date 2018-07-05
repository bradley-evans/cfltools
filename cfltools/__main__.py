import sys

def main():
    # Expermental code #
    # Don't judge me, I'm new to this. #
    print('in main')
    args = sys.argv[1:]
    print('argument count :: {}'.format(len(args)))
    for arg in args:
        print('passed argument :: {}'.format(arg))

