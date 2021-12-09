#!/usr/bin/env python3

import argparse


def main():
    """ Read in the seven segment data provided by the given file. Report
        the number of times 1, 4, 7, or 8 appear.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the seven segment data provided by the given file. Report\n" \
                  "the number of times 1, 4, 7, or 8 appear."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with seven segment display data.")

    args = parser.parse_args()

    ###########################################################################
    # Read in directions
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            seven_segment_data = [value.strip() for value in FILE.readlines()]
    except Exception:
        raise

    appearance_count = 0

    for seven_segment_datum in seven_segment_data:
        _, output_values = seven_segment_datum.split("|")
        output_values = output_values.strip().split()

        for output_value in output_values:
            if len(output_value) in {2, 3, 4, 7}:
                appearance_count += 1

    print("The numbers 1, 4, 7, or 8 appear {} times.".format(appearance_count))


if __name__ == '__main__':
    main()
