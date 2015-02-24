# -*- encoding: utf-8 -*-
import sys

from src.pyephem.propagator import Propagator
from src.utils.reader import TleReader


def main():
    from optparse import OptionParser

    parser = OptionParser(usage="%prog: [options]")
    parser.add_option(
        '-o', '--output_folder',
        help="Path to output folder", )
    parser.add_option(
        '-i', '--input_file', default=None,
        help="Path to file with satellites tle")
    parser.add_option('-s', '--start_time', default=None,
                      help="Start time, as string "
                           "(for example '2015-01-01 18:21:26')")
    parser.add_option('-e', '--end_time', default=None,
                      help="End time, as string "
                           "(for example '2015-01-01 18:21:26')")
    (options, args) = parser.parse_args()

    if options.input_file is None:
        print("Not found filename")
        sys.exit(-1)
    else:
        obj = TleReader()
        obj.read(options.input_file)
        Propagator(
            obj.get(), options.output_folder)


if __name__ == '__main__':
    main()
