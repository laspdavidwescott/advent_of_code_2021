#!/usr/bin/env python3

import argparse
import math


def calculate_fuel_spent(start_positions, end_position):
    """ Calculate the amount of fuel needed to get from the given start
        positions to the given end position.

        Input:  start positions [position <int>]
                end position <int>

        Output: fuel spent <int>
    """
    fuel_spent = 0

    for start_position in start_positions:
        fuel_spent += sum(range(abs(start_position - end_position) + 1))

    return fuel_spent


def main():
    """ Read in the crab horizontal positions provided by the given file.
        Report the position each crab can reach using the minimal amount of
        fuel.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the crab horizontal positions provided by the given file.\n" \
                  "Report the position each crab can reach using the minimal amount of\n" \
                  "fuel."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with crab horizontal positions.")

    args = parser.parse_args()

    ###########################################################################
    # Read in directions
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            crab_positions = list(map(int, FILE.read().strip().split(",")))
    except Exception:
        raise

    ###########################################################################
    # Find least fuel spent
    #
    # The idea here is to start at the lowest crab position and increment the
    # position by sqrt(max_position - min_position). We'll use this offset to
    # get close to the most fuel efficient position. As we increment the
    # position by the offset, the fuel usage will go down. Eventually the fuel
    # usage will start going back up. This means we've narrowed down the
    # position. Now we need to fine tune the position be decrementing the
    # position by 1 until we find the position with the minimum fuel usage.
    ###########################################################################

    # Get the min and max crab position values
    min_position = min(crab_positions)
    max_position = max(crab_positions)

    # Position and fuel usage we're looking for
    center_position = min_position
    center_fuel_spent = 0

    # Counter to make sure the while loop doesn't go on forever
    count = 0

    # Offset used to get close to the most fuel efficient position
    offset = int(math.sqrt(max_position - min_position))

    # Around we go!
    while count < len(crab_positions):
        # We're going to look at the positions just below and above
        lower_position = center_position - 1
        upper_position = center_position + 1

        # Find the fuel spent for the 3 positions
        center_fuel_spent = calculate_fuel_spent(crab_positions, center_position)
        upper_fuel_spent = calculate_fuel_spent(crab_positions, upper_position)
        lower_fuel_spent = calculate_fuel_spent(crab_positions, lower_position)

        # If the center fuel spent is in the middle of the lower and upper fuel
        # spent, we've found the position with the lowest fuel usage
        if lower_fuel_spent > center_fuel_spent < upper_fuel_spent:
            break
        # If we have gone too far with the larger initial offset, change the
        # offset so we decrement by 1 until we find the most fuel efficient
        # position
        elif center_fuel_spent < upper_fuel_spent:
            offset = -1

        # Update the center position
        center_position += offset

        # Increment the counter
        count += 1

    ###########################################################################
    # Report
    ###########################################################################

    print("Most fuel efficient meeting position: {}".format(center_position))
    print("Getting there uses this much fuel:    {}".format(center_fuel_spent))


if __name__ == '__main__':
    main()

