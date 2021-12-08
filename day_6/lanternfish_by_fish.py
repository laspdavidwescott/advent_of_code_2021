#!/usr/bin/env python3

import argparse


def main():
    """ Read in the lanternfish data provided by the given file. Report
        their growth over a certain number of days.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the lanternfish data provided by the given file. Report\n" \
                  "their growth over a certain number of days."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with initial lanternfish states")
    parser.add_argument("-d", "--days", type=int, help="Number of days of lanternfish growth", default=80)
    parser.add_argument("-g", "--gestation-period", type=int, help="Number of days before a new lanternfish is spawned", default=7)
    parser.add_argument("-m", "--maturation-period", type=int, help="Number of days before a lanternfish is matured", default=2)
    parser.add_argument("--debug", action='store_true', help="Enable debug mode")

    args = parser.parse_args()

    ###########################################################################
    # Read in directions
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            lanternfish_data = FILE.read().strip()
    except Exception:
        raise

    # The initial lanternfish timer values
    lanternfish_days = list(map(int, lanternfish_data.split(",")))

    # Debug
    if args.debug:
        lanternfish_days_string = ",".join(map(str, lanternfish_days))
        print("Initial State: {}".format(lanternfish_days_string))

    # Used in formatting below
    days_width = len(str(args.days))

    # Go through each day
    for day in range(1, args.days + 1):
        # Check each fish
        for index in range(len(lanternfish_days)):
            # If the fish's timer is at 0
            if lanternfish_days[index] == 0:
                # Reset the fish's timer to the gestation period
                lanternfish_days[index] = args.gestation_period - 1

                # Spawn new fish
                lanternfish_days.append(args.gestation_period - 1 + args.maturation_period)
            # Fish's timer is not 0
            else:
                # Decrement the timer
                lanternfish_days[index] -= 1

        # Debug
        if args.debug:
            days_string = "days:" if day > 1 else "day: "
            lanternfish_days_string = ",".join(map(str, lanternfish_days))
            print("After {:>{width}} {} {}".format(day, days_string, lanternfish_days_string, width=days_width))

    ###########################################################################
    # Report
    ###########################################################################

    print("Number of lanternfish after {} days: {}".format(args.days, len(lanternfish_days)))

    exit(0)


if __name__ == '__main__':
    main()
