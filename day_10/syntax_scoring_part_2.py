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

    # Scoring for illegal characters
    character_scores = {")": 1,
                        "]": 2,
                        "}": 3,
                        ">": 4}

    # A list of all the syntax line scores
    all_scores = []

    # Check each line of syntax
    for syntax_line in data:
        if args.debug:
            print("Checking syntax line '{}'".format(syntax_line))

        # Keep track of the current syntax line's status
        character_stack = []

        # Whether to skip the current line or not
        skip_syntax_line = False

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
                # Not the expected closing character, skip this syntax line
                else:
                    skip_syntax_line = True
                    break

        # Check if this line should be skipped
        if skip_syntax_line:
            if args.debug:
                print()

            # Skip this syntax line
            continue
        # Do not skip
        else:
            # Calculate the syntax line's score
            syntax_line_score = 0

            # Figure out the missing closing characters
            missing_characters = [characters[character] for character in character_stack]
            missing_characters.reverse()

            # Calculate the score
            for character in missing_characters:
                syntax_line_score *= 5
                syntax_line_score += character_scores[character]

            if args.debug:
                print("Missing closing characters: {}".format("".join(missing_characters)))
                print("Syntax line score: {}".format(syntax_line_score))

            all_scores.append(syntax_line_score)

        if args.debug:
            print()

    ###########################################################################
    # Report
    ###########################################################################

    # Sort the scores
    all_scores.sort()

    # Get the middle score
    middle_index = len(all_scores) // 2
    middle_score = all_scores[middle_index]

    print("The middle score is: {}".format(middle_score))


if __name__ == '__main__':
    main()
