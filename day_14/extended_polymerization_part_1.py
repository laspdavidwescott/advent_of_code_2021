#!/usr/bin/env python3

import argparse
import re


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
    parser.add_argument("-s", "--steps", type=int, help="Number of pair insertions to execute", default=10)
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

    # Evolve the polymer
    for step in range(args.steps):
        # The polymer with this step's insertions
        polymer_with_insertions = ""

        # Check each of the element pairs
        for index in range(len(polymer) - 1):
            # Get the 2 elements in the element pair
            element1 = polymer[index]
            element2 = polymer[index + 1]

            # Get the element to be inserted into the element pair
            inserted_element = insertion_rules.get("{}{}".format(element1, element2), "")

            # Add the updated element pair to the polymer
            polymer_with_insertions += "{}{}".format(element1, inserted_element)

        # Tack on the last element
        polymer = polymer_with_insertions + polymer[-1]

        if args.debug:
            print("Step {}: {}".format(step + 1, polymer))
            print()

    ###########################################################################
    # Determine most and least common elements in the polymer
    ###########################################################################

    # The element counts {element <str>: count <int>}
    element_counts = {}

    # Check each element in the polymer
    for element in polymer:
        # Count the element
        element_counts.setdefault(element, 0)
        element_counts[element] += 1

    # Sort the element counts
    sorted_element_counts = sorted(element_counts.items(), key=lambda x: x[1])

    ###########################################################################
    # Report
    ###########################################################################

    print("The most common element '{}' occurs '{}' times.".format(sorted_element_counts[-1][0], sorted_element_counts[-1][1]))
    print("The least common element '{}' occurs '{}' times.".format(sorted_element_counts[0][0], sorted_element_counts[0][1]))
    print()
    print("The difference between most and least common element counts is: {}".format(sorted_element_counts[-1][1] - sorted_element_counts[0][1]))

    exit(0)


if __name__ == '__main__':
    main()
