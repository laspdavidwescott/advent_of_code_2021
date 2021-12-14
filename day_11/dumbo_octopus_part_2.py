#!/usr/bin/env python3

import argparse


def increase_energy_levels(octopus_energy_levels, octopus_already_flashed):
    """ Increase the energy levels of each octopus if they have not already
        flashed.

        Input:  octopus energy levels [[energy level <int>]]
                octopus already flashed status [[has octopus flashed <bool>]]

        Output: None
    """
    # Check each octopus
    for row in range(len(octopus_energy_levels)):
        for column in range(len(octopus_energy_levels[row])):
            # If the octopus hasn't already flashed, increase their energy
            # level
            if not octopus_already_flashed[row][column]:
                octopus_energy_levels[row][column] += 1
            # Octopus has already flashed and therefore can't increase its
            # energy level
            else:
                continue


def print_data(octopus_energy_levels):
    """ Print the given data into a nice chart.

        Input:  octopus_energy_levels [[energy level <int>]]

        Output: None
    """
    # Find the widest energy level
    width = len(str(max([max(octopus_energy_levels[row]) for row in range(len(octopus_energy_levels))])))

    # Print every energy level in a nicely formatted grid
    for row in range(len(octopus_energy_levels)):
        for column in range(len(octopus_energy_levels[row])):
            print("{:>{width}} ".format(octopus_energy_levels[row][column], width=width), end="")

        print()


def propagate_flash(octopus_energy_levels, row, column, octopus_already_flashed):
    """ Propagate the flash that occurred at the given row and column. Keep
        track of whether additional flashes occurred.

        Input:  octopus energy levels [[energy level <int>]]
                row that flashed <int>
                column that flashed <int>
                octopus already flashed status [[has octopus flashed <bool>]]

        Output: None
    """
    # Reset the octopus's energy level
    octopus_energy_levels[row][column] = 0

    # Indicate that this octopus has flashed
    octopus_already_flashed[row][column] = True

    # Octopus energy level row and column counts
    row_count = len(octopus_energy_levels)
    column_count = len(octopus_energy_levels[0])

    # Get the coordinates of all the surrounding octopuses
    north = (row - 1, column) if 0 < row else None
    north_east = (row - 1, column + 1) if 0 < row and column < column_count - 1 else None
    east = (row, column + 1) if column < column_count - 1 else None
    south_east = (row + 1, column + 1) if row < row_count - 1 and column < column_count - 1 else None
    south = (row + 1, column) if row < row_count - 1 else None
    south_west = (row + 1, column - 1) if row < row_count - 1 and 0 < column else None
    west = (row, column - 1) if 0 < column else None
    north_west = (row - 1, column - 1) if 0 < row and 0 < column else None

    # Check each neighbor
    for coord in (north, north_east, east, south_east, south, south_west, west, north_west):
        # Skip if there is no neighboring octopus at these coordinates
        if coord is None:
            continue

        # Unpack the neighbor's row and column
        row_neighbor, column_neighbor = coord

        # If the neighbor hasn't already flashed, increase their energy level
        if not octopus_already_flashed[row_neighbor][column_neighbor]:
            octopus_energy_levels[row_neighbor][column_neighbor] += 1


def main():
    """ Read in the octopus energy levels provided by the given file.
        Report the number of times each octopus flashes during a given time
        frame.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the octopus energy levels provided by the given file.\n" \
                  "Report the number of times each octopus flashes during a given time\n" \
                  "frame."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with octopus energy levels data.")
    parser.add_argument("-s", "--max-steps", type=int, help="Maximum number of steps to evolve", default=100000)
    parser.add_argument("--debug", action='store_true', help="Enable debug")

    args = parser.parse_args()

    ###########################################################################
    # Read in lines of syntax
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            octopus_energy_levels = [list(map(int, list(value.strip()))) for value in FILE.readlines()]
    except Exception:
        raise

    # Make sure there is data
    if len(octopus_energy_levels) == 0:
        print("No octopus energy level data found in {}".format(args.file))
        exit(1)

    ###########################################################################
    # Process the energy levels for each step
    ###########################################################################

    if args.debug:
        print("#####  Initial Octopus Energy Levels  #####")
        print()
        print_data(octopus_energy_levels)
        print()

    # Octopus energy level row and column counts
    row_count = len(octopus_energy_levels)
    column_count = len(octopus_energy_levels[0])

    # Total octopus flash count
    flash_count = 0

    # Keep track of the current step number
    step = 0

    # Iterate over the maximum number of steps
    for _ in range(args.max_steps):
        step += 1

        if args.debug:
            print("#####  Step {}  #####".format(step))
            print()

        # Keep track of which octopuses have flashed in this step
        octopus_already_flashed = [[False] * column_count for _ in range(row_count)]

        ###########################################################################
        # Increase energy levels
        ###########################################################################

        # Increase energy levels of octopuses that have not already flashed
        increase_energy_levels(octopus_energy_levels, octopus_already_flashed)

        if args.debug:
            print("Step {} - Increase energy levels by 1".format(step))
            print_data(octopus_energy_levels)
            print()

        ###########################################################################
        # Propagate any flashes
        ###########################################################################

        # A status flag indicating whether to keep processing the energy levels
        # in this step
        keep_processing = True

        # Keep processing until no more flashes occur
        while keep_processing:
            # Assume processing stops
            keep_processing = False

            # Check each octopus energy level
            for row in range(row_count):
                for column in range(column_count):
                    # Skip this octopus if it has already flashed
                    if octopus_already_flashed[row][column]:
                        continue

                    # Octopus has flashed
                    if 9 < octopus_energy_levels[row][column]:
                        # Propagation will occur so we need to keep processing
                        keep_processing = True

                        # Update the flash count
                        flash_count += 1

                        # Propagate the flash
                        propagate_flash(octopus_energy_levels, row, column, octopus_already_flashed)

            if args.debug and keep_processing:
                print("Step {} - Flash Propagating".format(step))
                print_data(octopus_energy_levels)
                print()

        if args.debug:
            print("Step {} - Final State".format(step))
            print_data(octopus_energy_levels)
            print()

        # Check if all the octopuses have flashed in this step
        all_octopuses_flashed = all([all(octopus_already_flashed[row]) for row in range(len(octopus_already_flashed))])

        # If all octopuses have flashed in this step, stop
        if all_octopuses_flashed:
            break

    ###########################################################################
    # Report
    ###########################################################################

    print("All octopuses flashed at step {}".format(step))
    print("After {} steps, the flash count is: {}".format(step, flash_count))


if __name__ == '__main__':
    main()
