#!/usr/bin/env python3

import argparse

from cave import Cave


def find_paths(start_cave, end_cave, max_iterations=100000000):
    """ Find all the possible paths from the given start cave to the given end
        cave. Return all possible paths as lists of caves.

        Input:  start cave <Cave>
                end cave <Cave>
                max while loop iterations <int>

        Output: paths from start to end [[cave <Cave>]]
    """
    # A queue of possible cave paths
    cave_queue = [[start_cave]]

    # Paths that successfully go from start to end
    paths = []

    # Keep track of the current iteration count (to make sure the while loop
    # doesn't go off into infinity)
    iteration = 0

    # The name of the starting and ending caves
    start_cave_name = start_cave.getName()
    end_cave_name = end_cave.getName()

    # While there are paths to check
    while len(cave_queue) > 0 and iteration < max_iterations:
        # Increment me
        iteration += 1

        # Pull off the most recent list of caves (path) to check
        caves = cave_queue.pop(-1)

        # Get the most recent cave from the most recent list of caves (path)
        cave = caves[-1]

        # If we've reached the end, add the list of caves (path) to the
        # returned paths
        if cave.getName() == end_cave_name:
            paths.append(caves)

        # Get a list of the connecting caves
        connecting_caves = cave.getConnectingCaves()

        # Check all the connecting caves for possible paths
        for connecting_cave in connecting_caves:
            # The number of maximum allowed visits to a little cave. Start and
            # end caves are still only allowed 1 visit.
            max_visits = 2 if connecting_cave.getName() not in {start_cave_name, end_cave_name} else 1

            # If the cave is big (visit always allowed) or the cave hasn't
            # hasn't reached the visit limit.
            if connecting_cave.isBigCave() or caves.count(connecting_cave) < max_visits:
                # The next path of caves
                next_caves = caves + [connecting_cave]

                # The number of times little caves were visited
                little_cave_visit_counts = {}

                # Get the visit counts from the little caves in the upcoming
                # path
                for next_cave in next_caves:
                    if next_cave.isLittleCave():
                        little_cave_visit_counts.setdefault(next_cave.getName(), 0)
                        little_cave_visit_counts[next_cave.getName()] += 1

                # If visiting is allowed, add the path to the queue
                if len(little_cave_visit_counts) == 0 or sum(little_cave_visit_counts.values()) - len(little_cave_visit_counts) <= 1:
                    cave_queue.append(caves + [connecting_cave])

    # While loop went to infinity
    if max_iterations <= iteration:
        print("ERROR: Maximum allowed while loop iterations ({}) reached.".format(max_iterations))
        return []

    return paths


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

    ###########################################################################
    # Figure out all the cave connections
    ###########################################################################

    # All the cave names and their objects
    all_caves = {}

    # Go through each cave connection from the file
    for cave_connection in cave_connections:
        # Get the parent and child caves
        parent_cave, child_cave = cave_connection.split("-", 1)

        # If the parent hasn't been added yet, add it
        if parent_cave not in all_caves:
            all_caves[parent_cave] = Cave(parent_cave)

        # if the child hasn't been added yet, add it
        if child_cave not in all_caves:
            all_caves[child_cave] = Cave(child_cave)

        # Add the parent --> child connection to the parent cave (node)
        all_caves[parent_cave].addConnectingCave(all_caves[child_cave])

        # Add the child --> parent connection to the child cave (node)
        all_caves[child_cave].addConnectingCave(all_caves[parent_cave])

    if args.debug:
        print("#####  Cave Connections  #####")

        for cave_name in all_caves:
            connections = ",".join(["{}".format(cave.getName()) for cave in all_caves[cave_name].getConnectingCaves()])
            print("Cave '{}' --> {}".format(cave_name, connections))

        print()

    ###########################################################################
    # Find all the paths from start to end
    ###########################################################################

    # Get the starting and ending cave
    start_cave = all_caves['start']
    end_cave = all_caves['end']

    # Find all the paths
    paths = find_paths(start_cave, end_cave)

    if args.debug:
        print("#####  Paths from start to end  #####")

        for path in sorted(paths):
            print(" --> ".join((_cave.getName() for _cave in path)))

        print()

    ###########################################################################
    # Report
    ###########################################################################

    print("There are {} paths through the cave system.".format(len(paths)))

    exit(0)


if __name__ == '__main__':
    main()
