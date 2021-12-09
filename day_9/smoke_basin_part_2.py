#!/usr/bin/env python3

import argparse
import math


def find_basin_size(heightmap, coord):
    """ Find the size of the basin on the heightmap for the given coordinate.

        This is a recursive algorithm.

        Input:  heightmap [[height value <int>]]
                coordinate (row <int>, column <int>)

        Output: basin size <int>
    """
    # Unpack the row and column
    row, column = coord

    # Figure out the row and column counts
    row_count = len(heightmap)
    column_count = len(heightmap[0]) if row_count > 0 else 0

    # Figure out the 4 cardinal coordinates
    north_coord = (row - 1, column)
    south_coord = (row + 1, column)
    east_coord = (row, column + 1)
    west_coord = (row, column - 1)

    # Group coordinates together
    cardinal_coords = [north_coord, west_coord, south_coord, east_coord]

    # Get the height value for the given coordinate
    height_value = heightmap[row][column]

    # Keep track of all the basin coordinates; including the given coordinate
    basin_coords = set()
    basin_coords.add((row, column))

    # Check each direction
    for cardinal_coord in cardinal_coords:
        # Get the cardinal row and column
        cardinal_row, cardinal_column = cardinal_coord

        # If the cardinal coordinate goes off the heightmap, skip this
        # coordinate
        if cardinal_row < 0 or row_count <= cardinal_row or cardinal_column < 0 or column_count <= cardinal_column:
            continue

        # Get the cardinal height
        cardinal_height_value = heightmap[cardinal_row][cardinal_column]

        # If the cardinal height is lower than the given coordinate's height or
        # the cardinal height is 9 (not part of a basin), skip this coordinate
        if cardinal_height_value <= height_value or cardinal_height_value == 9:
            continue

        # If the basin keeps going in the directory of the cardinal coordinate
        if height_value < cardinal_height_value:
            # Look for more basin coordinates
            basin_coords.update(find_basin_size(heightmap, cardinal_coord))

    return basin_coords


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
    parser.add_argument("--basin-count", type=int, help="The top # of basins to multiply together", default=3)
    parser.add_argument("--debug", action='store_true', help="Print debug info")

    args = parser.parse_args()

    ###########################################################################
    # Read in directions
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            heightmap_data = [list(map(int, value.strip())) for value in FILE.readlines()]
    except Exception:
        raise

    ###########################################################################
    # Find all low points in the heightmap
    ###########################################################################

    # Keep track of total risk level and the low point coordinates
    total_risk_level = 0
    low_point_coords = []

    # Calculate the heightmap's row and column counts
    row_count = len(heightmap_data)
    column_count = len(heightmap_data[0]) if row_count > 0 else 0

    # Go through each coordinate in the heightmap
    for row in range(row_count):
        for column in range(column_count):
            # Get the height value
            value = heightmap_data[row][column]

            # Get and compare the height north of the coordinate
            north_value = heightmap_data[row - 1][column] if row - 1 >= 0 else 10
            is_less_than_north = value < north_value

            # Get and compare the height south of the coordinate
            south_value = heightmap_data[row + 1][column] if row + 1 < row_count else 10
            is_less_than_south = value < south_value

            # Get and compare the height east of the coordinate
            east_value = heightmap_data[row][column + 1] if column + 1 < column_count else 10
            is_less_than_east = value < east_value

            # Get and compare the height west of the coordinate
            west_value = heightmap_data[row][column - 1] if column - 1 >= 0 else 10
            is_less_than_west = value < west_value

            # If the coordinate's height is a low point if it's the lowest in
            # the immediate area
            if is_less_than_east and is_less_than_west and is_less_than_south and is_less_than_north:
                if args.debug:
                    print("Low Point ({}, {}) - Value: {}".format(row, column, value))
                    print("North Value: {} | South Value: {} | East Value: {} | West Value: {}".format(north_value, south_value, east_value, west_value))
                    print()

                # Add the low point coordinate
                low_point_coords.append((row, column))

                # Update the total risk level
                total_risk_level += value + 1

    if args.debug:
        print("Found {} low points.".format(len(low_point_coords)))
        print("Total risk level for all low points: {}".format(total_risk_level))
        print()

    ###########################################################################
    # Find basins and their sizes
    ###########################################################################

    # Keep a list of all the basin sizes
    basin_sizes = []

    # Search for basin coordinates starting at low points
    for coord in low_point_coords:
        # Find all the coordinates associated with this basin (recursively)
        basin_coords = find_basin_size(heightmap_data, coord)

        # The basin's size (coordinate count)
        basin_size = len(basin_coords)

        if args.debug:
            print("Basin Low Point: {}".format(coord))
            print("Basin Size:      {}".format(basin_size))
            print("Basin Coords:    {}".format(" ".join(map(str, basin_coords))))
            print()

        # Append the basin size
        basin_sizes.append(basin_size)

    ###########################################################################
    # Report
    ###########################################################################

    largest_basins = sorted(basin_sizes, reverse=True)[0:args.basin_count]
    print("The {} largest basin sizes are: {}".format(args.basin_count, " ".join(map(str, largest_basins))))
    print("The product of the 3 largest basins is: {}".format(math.prod(largest_basins)))


if __name__ == '__main__':
    main()
