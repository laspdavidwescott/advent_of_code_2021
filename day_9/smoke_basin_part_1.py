#!/usr/bin/env python3

import argparse


def main():
    """ Read in the heightmap provided by the given file. Find the lowest
        points in the map. Report the sum of the risk levels of all low points
        in the heightmap.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the heightmap provided by the given file. Find the lowest\n" \
                  "points in the map. Report the sum of the risk levels of all low points\n" \
                  "in the heightmap."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with heightmap data.")
    parser.add_argument("--debug", action='store_true', help="Print debug info")

    args = parser.parse_args()

    ###########################################################################
    # Read in heightmap data
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            heightmap_data = [list(map(int, value.strip())) for value in FILE.readlines()]
    except Exception:
        raise

    ###########################################################################
    # Find all low points in the heightmap
    ###########################################################################

    # Keep track of total risk level and the number of low points
    total_risk_level = 0
    low_point_count = 0

    # Calculate the heightmap's row and column counts
    row_count = len(heightmap_data)
    column_count = len(heightmap_data[0]) if row_count > 0 else 0

    # Go through each coordinate in the heightmap
    for row in range(row_count):
        for column in range(column_count):
            # Get the height value
            height = heightmap_data[row][column]

            # Get and compare the height north of the coordinate
            north_height = heightmap_data[row - 1][column] if row - 1 >= 0 else 10
            is_less_than_north = height < north_height

            # Get and compare the height south of the coordinate
            south_height = heightmap_data[row + 1][column] if row + 1 < row_count else 10
            is_less_than_south = height < south_height

            # Get and compare the height east of the coordinate
            east_height = heightmap_data[row][column + 1] if column + 1 < column_count else 10
            is_less_than_east = height < east_height

            # Get and compare the height west of the coordinate
            west_height = heightmap_data[row][column - 1] if column - 1 >= 0 else 10
            is_less_than_west = height < west_height

            # If the coordinate's height is a low point if it's the lowest in
            # the immediate area
            if is_less_than_east and is_less_than_west and is_less_than_south and is_less_than_north:
                if args.debug:
                    print("Low Point ({}, {}) - Value: {}".format(row, column, height))
                    print("North Value: {} | South Value: {} | East Value: {} | West Value: {}".format(north_height, south_height, east_height, west_height))
                    print()

                # Increment low point count
                low_point_count += 1

                # Update the total risk level
                total_risk_level += height + 1

    ###########################################################################
    # Report
    ###########################################################################

    print("Found {} low points.".format(low_point_count))
    print("Total risk level for all low points: {}".format(total_risk_level))


if __name__ == '__main__':
    main()
