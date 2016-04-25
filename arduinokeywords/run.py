import os
import sys

import argparse

from arduinokeywords import parse_header, parse_library, output_keywords, get_keywords_fullpath

# Setup command line parameters
parser = argparse.ArgumentParser(description='Generate a keywords.txt file for the Arduino IDE.')
parser.add_argument('-s', '--source', type=str, dest='source', metavar="dir", default=os.getcwd(),
                    help='Your library\'s root directory. Defaults to current directory')
parser.add_argument('-o', '--output', type=str, dest='output', metavar="dir", default="./",
                    help='The folder in which the keywords.txt file will be created. Defaults to --source')
parser.add_argument('-c', '--constant', type=str, dest='constants', default=[], action="append",
                    help='Specify additional constants to be written to keywords.txt. Multiple constants can be'
                         'defined by repeating this argument', metavar="CONSTANT")
parser.add_argument('-f', '--header', '--header-file', type=str, dest='headers', default=[], action="append",
                    help='Manually specify the header files to be parsed. Multiple files can be'
                         'defined by repeating this argument', metavar="file")
parser.add_argument('-d', '--depth', type=int, dest='depth', default=1,
                    help='Specify how deep the automatic header search should look')

args = parser.parse_args()

args.source = os.path.abspath(args.source)

if not os.path.exists(args.source):
    print("The source path {0} doesn't exist, quitting...".format(args.source))
    sys.exit(1)

if not os.path.isdir(args.source):
    print("The source path {0} isn't a directory, quitting...".format(args.source))
    sys.exit(1)

# If header files are specifed use those, otherwise search 'source' to a max depth of 'depth'
if len(args.headers) == 0:
    print("Searching for header files in {0}".format(args.source))
    print("Search max depth is: {0}".format(args.depth))

    classes = parse_library(args.source, args.depth)
else:
    print("Parsing the following header files:")
    classes = []
    for header in args.headers:
        print("\t{0}".format(header))
        try:
            classes.extend(parse_header(os.path.join(args.source, header)))
        except FileNotFoundError:
            print("\tFile {0} not found, skipping".format(header))

print()
print("Classes found: {0}".format(len(classes)))
print()

if len(args.constants) > 0:
    print("Additional constants:")
    for constant in args.constants:
        print("\t {0}".format(constant))

keywords_filename = get_keywords_fullpath(os.path.join(args.source, args.output))
print("Outputting keywords.txt to the following path")
print("\t{0}".format(keywords_filename))

output_keywords(classes, keywords_filename, args.constants)

print("Done")
