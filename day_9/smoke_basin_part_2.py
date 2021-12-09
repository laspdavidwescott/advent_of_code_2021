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
    row, column = coord

    row_count = len(heightmap)
    column_count = len(heightmap[0]) if row_count > 0 else 0

    north_coord = (row - 1, column)
    south_coord = (row + 1, column)
    east_coord = (row, column + 1)
    west_coord = (row, column - 1)

    directional_coords = [north_coord, west_coord, south_coord, east_coord]

    height_value = heightmap[row][column]

    basin_coords = set()
    basin_coords.add((row, column))

    for directional_coord in directional_coords:
        directional_row, directional_column = directional_coord

        if directional_row < 0 or row_count <= directional_row or directional_column < 0 or column_count <= directional_column:
            continue

        directional_height_value = heightmap[directional_row][directional_column]

        if directional_height_value <= height_value or directional_height_value == 9:
            continue

        if height_value < directional_height_value:
            basin_coords.update(find_basin_size(heightmap, directional_coord))

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
