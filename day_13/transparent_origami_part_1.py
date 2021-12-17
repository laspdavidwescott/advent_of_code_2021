#!/usr/bin/env python3

import argparse
import re
from copy import deepcopy


def print_dot_coordinates(dot_coordinates, use_dots=True):
    """ Print a grid of the given coordinates. A space " " or a dot "."
        indicate a blank coordinate. Octothorpes "#" indicate a coordinate in
        the given coordinates.

        Input:  coordinates [[(x coord <int>, y coord <int>]]
                use dots instead of blank space <bool>

        Output: None
    """
    # Determine the maximum x and y coordinates (size of grid)
    max_x_coord = max((coord[0] for coord in dot_coordinates))
    max_y_coord = max((coord[1] for coord in dot_coordinates))

    # Create the grid
    empty_char = "." if use_dots else " "
    grid = [[empty_char for _ in range(max_x_coord + 1)] for _ in range(max_y_coord + 1)]

    # Populate the grid from the given coordinates
    for x_coord, y_coord in sorted(dot_coordinates):
        grid[y_coord][x_coord] = "#"

    # Print the grid
    for row in grid:
        print("".join(list(map(str, row))))


def main():
    """ Read in the origami instructions provided by the given file.
        Report the number of visible dots after the first fold.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the origami instructions provided by the given file.\n" \
                  "Report the number of visible dots after the first fold."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with origami instructions.")
    parser.add_argument("-f", "--folds", type=int, help="Number of folds allowed", default=1)
    parser.add_argument("--debug", action='store_true', help="Enable debug")

    args = parser.parse_args()

    ###########################################################################
    # Read in lines of syntax
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            origami_instructions = [value.strip() for value in FILE.readlines()]
    except Exception:
        raise

    # Make sure there is data
    if len(origami_instructions) == 0:
        print("No origami instructions found in {}".format(args.file))
        exit(1)

    ###########################################################################
    # Parse the given origami instructions into dot coordinates and folds
    ###########################################################################

    # The dot coordinates and folding instructions
    dot_coordinates = set()
    folds = []

    # Parse the origami instructions
    for origami_instruction in origami_instructions:
        # If the instruction is blank, skip it
        if origami_instruction == "":
            continue

        # Check if it's a fold instruction
        fold_regex = re.search(r"fold\s+along\s+(\w+)=(\d+)", origami_instruction, re.I)

        # Fold instruction
        if fold_regex:
            folds.append((fold_regex.group(1), int(fold_regex.group(2))))
        # Dot coordinate
        else:
            # Convert coordinate from a string to a list of integers
            coordinate = tuple(map(int, origami_instruction.split(",")))
            dot_coordinates.add(coordinate)

    ###########################################################################
    # Fold!
    ###########################################################################

    # The number of folds executed
    fold_count = 0

    # Fold the coordinates
    for direction, line_coord in folds[0:args.folds]:
        # Keep track of the number of folds performed
        fold_count += 1

        # Check if the fold is in the x direction
        is_x_direction = direction.lower() == "x"

        # Make a copy of the dot coordinates
        temp_dot_coordinates = deepcopy(dot_coordinates)

        # Figure out what happens to each dot coordinate
        for dot_coordinate in dot_coordinates:
            # Unpack x and y coordinates
            x_coord, y_coord = dot_coordinate

            # Determine which coordinate to fold along (x or y)
            coord = x_coord if is_x_direction else y_coord

            # If the dot coordinate is at or after the folding coordinate,
            # remove the dot coordinate (we'll add the reflected one below)
            if line_coord <= coord:
                temp_dot_coordinates.remove(dot_coordinate)

            # If the dot coordinate needs to be reflected over the folding line
            if line_coord < coord:
                # Determine if the x or y coordinate needs to be reflected
                reflected_dot_coordinate = (x_coord - (x_coord - line_coord) * 2, y_coord) if is_x_direction else (x_coord, y_coord - (y_coord - line_coord) * 2)

                # Make sure the reflected dot doesn't go off the grid
                if 0 <= reflected_dot_coordinate[0] and 0 <= reflected_dot_coordinate[1]:
                    temp_dot_coordinates.add(reflected_dot_coordinate)

        # Update the dot coordinates
        dot_coordinates = deepcopy(temp_dot_coordinates)

    ###########################################################################
    # Report
    ###########################################################################

    if args.debug:
        print_dot_coordinates(dot_coordinates)
        print()

    print("The number of dots left after {} fold{} is: {}".format(fold_count, "s" if fold_count > 1 else "", len(dot_coordinates)))


if __name__ == '__main__':
    main()
