#!/usr/bin/env python3

import argparse
import re
from copy import deepcopy
import math


def main():
    """ Read in the polymer instructions provided by the given file.
        Figure out the polymer based on the given instructions. Report the
        most common element count minus the least common element count.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the polymer instructions provided by the given file.\n" \
                  "Figure out the polymer based on the given instructions. Report the\n" \
                  "most common element count minus the least common element count."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with polymer instructions.")
    parser.add_argument("-s", "--steps", type=int, help="Number of pair insertions to execute", default=40)
    parser.add_argument("--debug", action='store_true', help="Enable debug")

    args = parser.parse_args()

    ###########################################################################
    # Read in lines of syntax
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            polymer_instructions = [value.strip() for value in FILE.readlines()]
    except Exception:
        raise

    # Make sure there is data
    if len(polymer_instructions) == 0:
        print("No polymer instructions found in {}".format(args.file))
        exit(1)

    ###########################################################################
    # Parse the polymer instructions into polymer template and paired
    # insertion rules
    ###########################################################################

    # The initial polymer template is from line 1
    polymer = polymer_instructions[0]

    # The element insertion rules { element_pair <str> : inserted element <str> }
    insertion_rules = {}

    # Go through the rest of the instructions
    for polymer_instruction in polymer_instructions:
        # Check for an insertion rule
        regex_rule = re.search(r"(\w+)\s+->\s+(\w+)", polymer_instruction)

        # If an insertion rule was found, add it
        if regex_rule:
            insertion_rules[regex_rule.group(1)] = regex_rule.group(2)

    if args.debug:
        print("Polymer template: {}".format(polymer))

        for element_pair, inserted_element in insertion_rules.items():
            print("{} -> {}".format(element_pair, inserted_element))

        print()

    ###########################################################################
    # Insert elements
    ###########################################################################

    # Keep track of the element pair counts {element pair <str>: count <int>}
    element_pair_counts = {element_pair: 0 for element_pair in insertion_rules.keys()}

    # Count the element pairs in the initial polymer
    for index in range(len(polymer) - 1):
        element_pair = polymer[index] + polymer[index + 1]
        element_pair_counts[element_pair] += 1

    # Evolve the polymer
    for step in range(args.steps):

        # A copy of the element pair counts (because the original is modified
        # and used in the loop below)
        temp_element_pair_counts = deepcopy(element_pair_counts)

        # Check each element pair to see if an element should be inserted
        for element_pair, count in temp_element_pair_counts.items():
            # Insert elements into existing element pairs
            if count > 0:
                # Get the elements of the element pair and the inserted element
                element1, element2 = list(element_pair)
                inserted_element = insertion_rules[element_pair]

                # When an element is inserted, the original element pair is
                # destroyed
                element_pair_counts[element_pair] -= count

                # Increment the new element pairs
                element_pair_counts[element1 + inserted_element] += count
                element_pair_counts[inserted_element + element2] += count

        if args.debug:
            print("Step {}".format(step + 1))

            for element_pair, count in element_pair_counts.items():
                print("    {} --> {}".format(element_pair, count))

            print()

    ###########################################################################
    # Determine most and least common elements in the polymer
    ###########################################################################

    # The element counts {element <str>: count <int>}
    element_counts = {}

    # Count each element in the element pair
    for element_pair, count in element_pair_counts.items():
        # Elements of the element pair
        element1, element2 = list(element_pair)

        # Add in the elements
        element_counts.setdefault(element1, 0)
        element_counts.setdefault(element2, 0)

        # Increment the elements' counts
        element_counts[element1] += count
        element_counts[element2] += count

    # Each of the counts need to be halved (HB+BC is actually HBC not HBBC)
    element_counts = {element: math.ceil(count / 2) for element, count in element_counts.items()}

    # Sort the elements by their counts
    sorted_elements = sorted(element_counts.items(), key=lambda x: x[1])

    ###########################################################################
    # Report
    ###########################################################################

    print("The most common element '{}' occurs '{}' times.".format(sorted_elements[-1][0], sorted_elements[-1][1]))
    print("The least common element '{}' occurs '{}' times.".format(sorted_elements[0][0], sorted_elements[0][1]))
    print()
    print("The difference between most and least common element counts is: {}".format(sorted_elements[-1][1] - sorted_elements[0][1]))

    exit(0)


if __name__ == '__main__':
    main()
