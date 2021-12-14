#!/usr/bin/env python3

import argparse


class Cave(object):
    def __init__(self, name):
        self.__name = name
        self.__connecting_caves = []

    def addConnectingCave(self, cave):
        """ Add a cave that connects to this cave.

            Input:  cave <Cave>

            Output: None
        """
        # Check if the given cave is already connected to this cave
        if cave not in self.__connecting_caves:
            self.__connecting_caves.append(cave)
        else:
            print("Cave connection already exists {} --> {}".format(self.getName(), cave.getName()))

    def getConnectingCaves(self):
        """ Return the caves that connect to this cave.

            Input:  None

            Output: connecting caves [cave <Cave>]
        """
        return self.__connecting_caves

    def getName(self):
        """ Return the name of this cave.

            Input:  None

            Output: cave name <str>
        """
        return self.__name

    def isBigCave(self):
        """ Return if this is a big cave or not.

            Input:  None

            Output: is a big cave <bool>
        """
        return self.__name == self.__name.upper()


def main():
    """ Read in the cave connection data provided by the given file.
        Report the number possible passages.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the cave connection data provided by the given file.\n" \
                  "Report the number possible passages."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with cave connection data.")
    parser.add_argument("--debug", action='store_true', help="Enable debug")

    args = parser.parse_args()

    ###########################################################################
    # Read in lines of syntax
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            cave_connections = [value.strip() for value in FILE.readlines()]
    except Exception:
        raise

    # Make sure there is data
    if len(cave_connections) == 0:
        print("No cave connection data found in {}".format(args.file))
        exit(1)

    all_caves = {}

    for cave_connection in cave_connections:
        parent_cave, child_cave = cave_connection.split("-", 1)

        if parent_cave not in all_caves:
            all_caves[parent_cave] = Cave(parent_cave)

        if child_cave not in all_caves:
            all_caves[child_cave] = Cave(child_cave)

        all_caves[parent_cave].addConnectingCave(all_caves[child_cave])
        all_caves[child_cave].addConnectingCave(all_caves[parent_cave])

    for cave_name in all_caves:
        print("#####  {}  #####".format(cave_name))
        print("\n".join(["{} {}".format(cave.getName(), cave.isBigCave()) for cave in all_caves[cave_name].getConnectingCaves()]))
        print()


if __name__ == '__main__':
    main()
