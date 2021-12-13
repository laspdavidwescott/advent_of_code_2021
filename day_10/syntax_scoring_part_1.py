#!/usr/bin/env python3

import argparse


def main():
    """ Read in the navigation subsystem syntax provided by the given file.
        Report the syntax score by counting the number of corrupt syntax lines.
        A line is corrupt if the line contains an incorrect closing character.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the navigation subsystem syntax provided by the given file.\n" \
                  "Report the syntax score by counting the number of corrupt syntax lines.\n" \
                  "A line is corrupt if the line contains an incorrect closing character."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with navigation subsystem syntax data.")
    parser.add_argument("--debug", action='store_true', help="Enable debug")

    args = parser.parse_args()

    ###########################################################################
    # Read in lines of syntax
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            data = [value.strip() for value in FILE.readlines()]
    except Exception:
        raise

    ###########################################################################
    # Parse the navigation subsystem syntax lines
    ###########################################################################

    # Opening characters and their closing counterparts
    characters = {"{": "}",
                  "[": "]",
                  "(": ")",
                  "<": ">"}

    # Keep track of the number of illegal characters found
    illegal_charaters = {character: 0 for character in characters.values()}

    # Check each line of syntax
    for syntax_line in data:
        if args.debug:
            print("Checking syntax line '{}'".format(syntax_line))

        # Keep track of the current syntax line's status
        character_stack = []

        # Check each character in the syntax line
        for character_index, character in enumerate(syntax_line):
            # If an opening character, add to the stack
            if character in characters.keys():
                character_stack.append(character)
            # If a closing character
            elif character in characters.values():
                # Determine if this is the expected closing character
                expected_charater = characters[character_stack[-1]]

                # If closing character is as expected, remove opening and
                # closing characters from stack
                if expected_charater == character:
                    character_stack.pop(-1)
                # Not the expected closing character, record illegal character
                else:
                    illegal_charaters[character] += 1

                    if args.debug:
                        print("Illegal character found at character index {}. Expected: {}, found {}.".format(character_index, expected_charater, character))
                    break

        if args.debug:
            if len(character_stack) == 0:
                print("Syntax looks good!")
            else:
                print("Missing closing characters for: {}".format(",".join(character_stack)))

            print()

    ###########################################################################
    # Report
    ###########################################################################

    # Scoring for illegal characters
    character_scores = {")": 3,
                        "]": 57,
                        "}": 1197,
                        ">": 25137}

    total_score = 0

    for illegal_charater, count in illegal_charaters.items():
        character_score = count * character_scores[illegal_charater]
        print("{}x {} --> {} points".format(count, illegal_charater, character_score))

        total_score += character_score

    print()
    print("Total syntax error score: {}".format(total_score))


if __name__ == '__main__':
    main()
