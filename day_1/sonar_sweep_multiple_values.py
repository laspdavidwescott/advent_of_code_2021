#!/usr/bin/env python3

import argparse


def main():
    """ Read in a file that contains water depth values. Each value is an
        integer. One value per line of the file. Determine how many times the
        depth increases by comparing 3 depth values.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in depth values from the given file. Find and count 3-value depth increases."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", help="Text file with depth values. One value per line.")
    parser.add_argument("-n", "--number", type=int, help="Number of values to add together for comparison", default=3)

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
    if len(depth_values) < args.number + 1:
        print("Not enough depth values to check for increases in depth.")
        exit(1)

    # Number of times the depth increased
    depth_increase_count = 0

    # Check each value. Compare 2 values at a time. If the current value is
    # less than the next value, that's an increase. Count it.
    for index in range(0, len(depth_values) - args.number):
        # The two values to compare are summations of depth values. The number
        # values in the summation was given at the command line (-n). Default
        # is 3 values per summation.
        depth_values_summary1 = sum(depth_values[index:index+args.number])
        depth_values_summary2 = sum(depth_values[index+1:index+1+args.number])

        # Check if the values increase
        does_depth_increase = depth_values_summary1 < depth_values_summary2

        # Increment count when depth increases
        if does_depth_increase:
            depth_increase_count += 1

    ###########################################################################
    # Report
    ###########################################################################

    print("Reading values from the file: {}".format(args.file))
    print("Number of values to consider: {}".format(args.number))
    print("Total number of depth values: {}".format(len(depth_values)))
    print("Number of depth increases is: {}".format(depth_increase_count))

    exit(0)


if __name__ == "__main__":
    main()
