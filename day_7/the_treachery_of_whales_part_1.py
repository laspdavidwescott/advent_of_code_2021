#!/usr/bin/env python3

import argparse


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
    # Find the most fuel efficient position
    ###########################################################################

    # Get the min and max crab position values
    min_position = min(crab_positions)
    max_position = max(crab_positions)

    # Keep track of the best position and best fuel usage
    best_position = -1
    best_fuel_spent = sum(crab_positions)

    # Check each possible meeting position between the min and max crab positions
    for meeting_position in range(min_position, max_position + 1):
        # Keep track of the fuel spent for the current meeting position
        current_fuel_spent = 0

        # Check how much fuel is used to get from each crab position to the
        # current meeting position
        for crab_position in crab_positions:
            current_fuel_spent += abs(crab_position - meeting_position)

        # If the current fuel consumption is lower than the best fuel consumption
        if current_fuel_spent < best_fuel_spent:
            # Update the best fuel and position values
            best_fuel_spent = current_fuel_spent
            best_position = meeting_position

    ###########################################################################
    # Report
    ###########################################################################

    print("Most fuel efficient meeting position: {}".format(best_position))
    print("Getting there uses this much fuel:    {}".format(best_fuel_spent))


if __name__ == '__main__':
    main()

