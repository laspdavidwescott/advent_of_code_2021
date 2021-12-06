#!/usr/bin/env python3

import argparse
import re


def main():
    """ Read in the hydrothermal vent data provided by the given file. Report
        the number of most dangerous locations (2 or more hydrothermal lines
        intersect).
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the hydrothermal vent data provided by the given file. Report\n" \
                  "the number of most dangerous locations (2 or more hydrothermal lines\n" \
                  "intersect).\n"

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with hydrothermal vent data.")
    parser.add_argument("-l", "--limit", type=int, help="Line crossings limit (at this number and above is dangerous)", default=2)

    args = parser.parse_args()

    ###########################################################################
    # Read in directions
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            hydrothermal_vent_data = [value.strip() for value in FILE.readlines()]
    except Exception:
        raise

    ###########################################################################
    # Find and count hydrothermal line crossings
    ###########################################################################

    # The hydrothermal vent coordinates (key) and line crossing counts (value)
    coordinates = {}

    # Check each hydrothermal vent line
    for line in hydrothermal_vent_data:
        # Look for line coordinates
        regex = re.search(r"(\d+),(\d+)\s+->\s+(\d+),(\d+)", line)

        # If coordinates were found
        if regex:
            # Get the 2 sets of coordinates
            x_coord1 = int(regex.group(1))
            y_coord1 = int(regex.group(2))
            x_coord2 = int(regex.group(3))
            y_coord2 = int(regex.group(4))

            # Skip lines that aren't horizontal or vertical
            if x_coord1 != x_coord2 and y_coord1 != y_coord2:
                continue

            # Vertical hydrothermal line
            if x_coord1 == x_coord2:
                # Count the original coordinates and all coordinates in between
                for y_coord in range(min(y_coord1, y_coord2), max(y_coord1, y_coord2) + 1):
                    # X coordinate is constant; Y coordinate varies
                    coords = (x_coord1, y_coord)
                    coordinates.setdefault(coords, 0)
                    coordinates[coords] += 1
            # Non-vertical hydrothermal line
            else:
                slope = (y_coord2 - y_coord1) / (x_coord2 - x_coord1)
                y_intercept = y_coord1 - slope * x_coord1

                for x_coord in range(min(x_coord1, x_coord2), max(x_coord1, x_coord2) + 1):
                    y_coord = slope * x_coord + y_intercept
                    coords = (x_coord, y_coord)
                    coordinates.setdefault(coords, 0)
                    coordinates[coords] += 1
        # Invalid hydrothermal vent line
        else:
            print("Invalid hydrothermal line coordinates: '{}'".format(line))

    ###########################################################################
    # Count the number of dangerous line crossings
    ###########################################################################

    # Total number of dangerous hydrothermal line crossings
    dangerous_line_crossing_count = 0

    # Check each coordinate's count
    for coord, count in coordinates.items():
        # If a dangerous hydrothermal line crossing was found
        if count >= args.limit:
            dangerous_line_crossing_count += 1

    ###########################################################################
    # Report
    ###########################################################################

    print("Total number of dangerous hydrothermal line crossings: {}".format(dangerous_line_crossing_count))

    exit(0)



if __name__ == '__main__':
    main()
