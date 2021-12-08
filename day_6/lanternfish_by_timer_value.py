#!/usr/bin/env python3

import argparse
import math


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
    parser.add_argument("-d", "--days", type=int, help="Number of days of lanternfish growth", default=256)
    parser.add_argument("-g", "--gestation-period", type=int, help="Number of days before a new lanternfish is spawned", default=7)
    parser.add_argument("-m", "--maturation-period", type=int, help="Number of days before a lanternfish is matured", default=2)
    parser.add_argument("--debug", action='store_true', help="Enable debug mode")

    args = parser.parse_args()

    ###########################################################################
    # Read in directions
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            lanternfish_data = list(map(int, FILE.read().strip().split(",")))
    except Exception:
        raise

    # Keep track of the number of fish per timer countdown value
    timer_counts = [0] * (args.gestation_period + args.maturation_period)

    # Add in the initial lanternfish timer values
    for lanternfish_datum in lanternfish_data:
        timer_counts[lanternfish_datum] += 1

    # Debug
    if args.debug:
        print("Initial:", timer_counts)

    # For use with formatting below
    days_width = len(str(args.days))

    # Go through each day
    for day in range(1, args.days + 1):
        # The number of new fish for this day
        new_fish_count = timer_counts[0]

        # Shift all the timer counts
        for index in range(len(timer_counts) - 1):
            timer_counts[index] = timer_counts[index+1]

        # Fish that just spawned, reset their timers to the gestation period
        timer_counts[args.gestation_period - 1] += new_fish_count

        # Add in all the newly spawned fish (gestation period + maturation period)
        timer_counts[args.gestation_period + args.maturation_period - 1] = new_fish_count

        # Debug
        if args.debug:
            print("Day {:>{width}}  ".format(day, width=days_width), timer_counts)

    ###########################################################################
    # Report
    ###########################################################################

    print("Number of lanternfish after {} days is: {}".format(args.days, sum(timer_counts)))

    exit(0)


if __name__ == '__main__':
    main()
