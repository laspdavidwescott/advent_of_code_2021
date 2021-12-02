#!/usr/bin/env python3

import argparse
import re


def main():
    """ Read in the piloting instructions provided by the given file. Report
        the submarine's final position.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the piloting instructions provided by the given file. Report the submarine's final position."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", help="Text file with depth values. One value per line.")

    args = parser.parse_args()

    ###########################################################################
    # Read in directions
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            directions = FILE.readlines()
    except Exception:
        raise

    ###########################################################################
    # Calculate submarine location
    ###########################################################################

    # The depth and horizontal positions
    depth_position = 0
    horizontal_position = 0

    # Analyze each direction
    for direction in directions:
        # Split the direction into command and value
        command, value = re.split(r"\s+", direction.strip())

        # Sanitize the value and command
        value = int(value)
        command = command.lower()

        # Horizontal forward
        if command == "forward":
            horizontal_position += value
        # Depth down
        elif command == "down":
            depth_position += value
        # Depth up
        elif command == "up":
            depth_position -= value
        # Unknown command
        else:
            print("ERROR: Unrecognized command: {}".format(command))

    ###########################################################################
    # Report
    ###########################################################################

    print("Depth Position:      {}".format(depth_position))
    print("Horizontal Position: {}".format(horizontal_position))
    print("Multiplied Together: {}".format(depth_position * horizontal_position))

    exit(0)


if __name__ == '__main__':
    main()
