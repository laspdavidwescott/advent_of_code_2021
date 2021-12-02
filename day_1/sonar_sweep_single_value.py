#!/usr/bin/env python3

import argparse


def main():
    """ Read in a file that contains water depth values. Each value is an
        integer. One value per line of the file. Determine how many times the
        depth increases by comparing 1 depth value at a time.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in depth values from the given file. Find and count single value depth increases."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", help="Text file with depth values. One value per line.")

    args = parser.parse_args()

    ###########################################################################
    # Read in and convert values
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            depth_values = FILE.readlines()

            # Convert values to integers
            depth_values = list(map(int, depth_values))
    except Exception:
        raise

    ###########################################################################
    # Determine number of depth increases
    ###########################################################################

    # Check if there are enough values to calculate at least one depth increase
    if len(depth_values) < 2:
        print("Not enough depth values to check for increases in depth.")
        exit(1)

    # Number of times the depth increased
    depth_increase_count = 0

    # Check each value. Compare 2 values at a time. If the current value is
    # less than the next value, that's an increase. Count it.
    for index in range(0, len(depth_values)-1):
        # The current and next depth values
        depth_value1 = depth_values[index]
        depth_value2 = depth_values[index+1]

        # Check if the values increase
        does_depth_increase = depth_value1 < depth_value2

        # Increment count when depth increases
        if does_depth_increase:
            depth_increase_count += 1

    ###########################################################################
    # Report
    ###########################################################################

    print("Reading values from the file: {}".format(args.file))
    print("Total number of depth values: {}".format(len(depth_values)))
    print("Number of depth increases is: {}".format(depth_increase_count))

    exit(0)


if __name__ == "__main__":
    main()
