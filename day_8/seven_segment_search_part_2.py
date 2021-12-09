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

    ###########################################################################
    # Plug and chug
    ###########################################################################

    # Correct segment to digit mapping
    segments_to_digit = {"abcefg": "0",
                          "cf": "1",
                          "acdeg": "2",
                          "acdfg": "3",
                          "bcdf": "4",
                          "abdfg": "5",
                          "abdefg": "6",
                          "acf": "7",
                          "abcdefg": "8",
                          "abcdfg": "9"}

    # Keep a running total of the displayed numbers
    total_output_value = 0

    # Go through each set of data (observed signal patterns and output value)
    for seven_segment_datum in seven_segment_data:

        ###########################################################################
        # Figure out the "bad" segment to "good" segment mapping
        ###########################################################################

        # Pull out the signal patterns and output values from the data. Convert
        # the signal patterns into a list of sets where each signal letter is a
        # value in the set.
        signal_patterns, output_values = seven_segment_datum.split("|")
        signal_patterns = list(map(set, sorted(("".join(sorted(value)) for value in signal_patterns.strip().split()), key=len)))
        output_values = output_values.strip().split()

        # A mapping of "bad" signals to correct segments
        signal_to_segment_map = {}

        # Find the "a" (top) mapping
        signal = signal_patterns[1].difference(signal_patterns[0]).pop()
        signal_to_segment_map[signal] = "a"

        # Find the "d" (middle) mapping
        signal = signal_patterns[2].intersection(signal_patterns[3], signal_patterns[4], signal_patterns[5]).pop()
        signal_to_segment_map[signal] = "d"

        # Find the "g" (bottom) mapping
        signal = signal_patterns[3].intersection(signal_patterns[4], signal_patterns[5]).difference(set(signal_to_segment_map)).pop()
        signal_to_segment_map[signal] = "g"

        # Find the "b" (upper left) mapping
        signal = signal_patterns[6].intersection(signal_patterns[7], signal_patterns[8]).difference(set(signal_to_segment_map)).difference(signal_patterns[0]).pop()
        signal_to_segment_map[signal] = "b"

        # Find the "f" (lower right) mapping
        signal = signal_patterns[6].intersection(signal_patterns[7], signal_patterns[8]).difference(set(signal_to_segment_map)).pop()
        signal_to_segment_map[signal] = "f"

        # Find the "c" (upper right) mapping
        signal = signal_patterns[0].difference(set(signal_to_segment_map)).pop()
        signal_to_segment_map[signal] = "c"

        # Find the "e" (lower left) mapping
        signal = signal_patterns[9].difference(set(signal_to_segment_map)).pop()
        signal_to_segment_map[signal] = "e"

        ###########################################################################
        # Figure out the displayed number
        ###########################################################################

        # The displayed number
        number = ""

        # Process each output value (digit)
        for output_value in output_values:
            # The displayed segments
            segments = ""

            # Piece together the corrected segments
            for segment in output_value:
                segments += signal_to_segment_map[segment]

            # Sort the segments (so they work with the segments-to-digit map)
            segments = "".join(sorted(segments))

            # Append the digit to the displayed number
            number += segments_to_digit[segments]

        # Convert the displayed number to an integer
        number = int(number)

        print("Displayed number: {}".format(number))

        # Add the currently displayed number to the total output value
        total_output_value += number

    ###########################################################################
    # Report
    ###########################################################################

    print()
    print("Total of all output values: {}".format(total_output_value))

    exit(0)


if __name__ == '__main__':
    main()
