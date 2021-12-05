#!/usr/bin/env python3

import argparse
import re


class BingoCard(object):
    """ A class that represents the state of a Bingo board. This class will
        keep track of whether a board has bingo or not.

        Input:  bingo board numbers [row of numbers [ number <int> ]]
    """
    def __init__(self, numbers):
        # Number of rows and columns on the card
        self.__row_count = len(numbers)
        self.__column_count = len(numbers[0])

        # Break up the card's numbers into coordinates
        self.__numbers_coords = {int(numbers[row][col]): (row, col) for row in range(self.__row_count) for col in range(self.__column_count)}

        # The unmarked card numbers
        self.__unmarked_numbers = set(self.__numbers_coords.keys())

        # Keep track of how many numbers have been marked in each row and column.
        self.__bingo_row_counts = [0] * self.__row_count
        self.__bingo_column_counts = [0] * self.__column_count

    def calculateFinalScore(self, winning_number):
        """ Calculate the final score using the given winning drawn number.

            Input:  winning drawn number <int>

            Output: final score <int>
        """
        # Calculate the final score by add up all the numbers in the card and
        # multiplying the result by the given winning drawn number.
        final_score = sum(self.__unmarked_numbers) * winning_number

        return final_score

    def checkForBingo(self):
        """ Check the card for Bingo.

            Input:  None

            Output: is there bingo <bool>
                    rows and/or columns with bingo (row numbers {<int>}, column numbers {<int>})
        """
        is_there_bingo = False
        bingos = (set(), set())

        # Check the Bingo row counts
        for row, bingo_row_count in enumerate(self.__bingo_row_counts):
            # If all the numbers in a row have been marked, BINGO!
            if bingo_row_count == self.__row_count:
                bingos[0].add(row)
                is_there_bingo = True

        # Check the Bingo column counts
        for column, bingo_column_count in enumerate(self.__bingo_column_counts):
            # If all the numbers in a column have been marked, BINGO!
            if bingo_column_count == self.__column_count:
                bingos[1].add(column)
                is_there_bingo = True

        return is_there_bingo, bingos

    def markNumber(self, number):
        """ Mark a number, if it exists, on the Bingo card.

            Input:  number <int>

            Output: None
        """
        # Check if the number is on the card
        if number in self.__numbers_coords:

            # Remove the marked number
            self.__unmarked_numbers.remove(number)

            # Get the card row and column where the number is located
            row, column = self.__numbers_coords[number]

            # Increment the row and column counters for the number's coordinates
            self.__bingo_row_counts[row] += 1
            self.__bingo_column_counts[column] += 1

    def print_card(self):
        """ Print the card. Mark if there are any Bingos.

            Input:  None

            Output: None
        """
        # Get the rows and/or columns with Bingo
        _, bingos = self.checkForBingo()
        rows_with_bingo = bingos[0]
        columns_with_bingo = bingos[1]

        # Calculate the column width
        column_width = 4 if len(rows_with_bingo) > 0 else 2

        # Reverse the numbers ==> coordinates to coordinates ==> numbers
        coords_numbers = {coords: number for number, coords in self.__numbers_coords.items()}

        # Keep track of the previous iteration's row
        previous_row = 0

        # Go through all the numbers' coordinates
        for coord in sorted(coords_numbers):
            # Row and column
            row, column = coord

            # Number at the coordinate
            number = coords_numbers[coord]

            # Check if the row changed
            if row != previous_row:
                print()
                previous_row = row

            # If the row or column has Bingo, put parenthesis around the number
            if row in rows_with_bingo or column in columns_with_bingo:
                print("({:>2}) ".format(number), end="")
            # Not a number that's part of a Bingo
            else:
                print("{:>{width}} ".format(number, width=column_width), end="")

        print()


def main():
    """ Read in the Bingo numbers provided by the given file. Report which
        Bingo card wins by adding all the winning card's numbers then
        multiplying by the winning number.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the Bingo numbers provided by the given file. Report which\n" \
                  "Bingo card wins by adding all the winning card's numbers then\n" \
                  "multiplying by the winning number."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with Bingo numbers.")
    parser.add_argument("-r", "--rows", help="Number of rows in a card", default=5)
    parser.add_argument("-c", "--columns", help="Number of columns in a card", default=5)

    args = parser.parse_args()

    ###########################################################################
    # Read in directions
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            bingo_data = [value.strip() for value in FILE.readlines()]
    except Exception:
        raise

    ###########################################################################
    # Parse the Bingo numbers
    ###########################################################################

    # Get the drawn numbers from the input file
    drawn_numbers = bingo_data[0].split(",")

    # All the Bingo cards
    bingo_cards = []

    # Current Bingo card numbers
    bingo_card_numbers = []

    # Go through the Bingo data (skip first 2 lines; they are drawn numbers data)
    for line in bingo_data[2:]:
        # Not an empty line
        if line.strip() != "":
            # Add the row of Bingo numbers
            bingo_card_numbers.append(re.split(r"\s+", line))

        # If enough rows have been accumulated
        if len(bingo_card_numbers) == args.rows:
            # Create a new Bingo card
            bingo_cards.append(BingoCard(bingo_card_numbers))

            # Clear the Bingo card numbers for the next card
            bingo_card_numbers = []

    print("Drawing Numbers: ", end="")

    # Keep track of the order each card gets Bingo
    cards_with_bingo = []

    # Drawn numbers
    for drawn_number in drawn_numbers:
        # Make sure the drawn number is an integer
        drawn_number = int(drawn_number)

        print("{} ".format(drawn_number), end="")

        # Play each Bingo card
        for bingo_card in bingo_cards:
            # Mark the drawn number on the Bingo card
            bingo_card.markNumber(drawn_number)

            # Check if this card has Bingo and report if it does
            if bingo_card.checkForBingo()[0] and bingo_card not in cards_with_bingo:
                cards_with_bingo.append(bingo_card)

        # If the last card gets Bingo
        if len(cards_with_bingo) == len(bingo_cards):
            print("\n")
            print("***************")
            print("* LAST BINGO! *")
            print("***************")
            print()
            cards_with_bingo[-1].print_card()
            print()
            print("Final Score: {}".format(cards_with_bingo[-1].calculateFinalScore(drawn_number)))

            # Stop the loop
            break

    exit(0)


if __name__ == '__main__':
    main()
