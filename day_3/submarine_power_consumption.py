#!/usr/bin/env python3

import argparse


def main():
    """ Read in the submarine diagnostics provided by the given file. Report
        the submarine's power consumption by first determining the gamma and
        epsilon rates. Then multiply them together to get the power rating.
    """
    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the submarine diagnostics provided by the given file. Report\n" \
                  "the submarine's power consumption by first determining the gamma and\n" \
                  "epsilon rates. Then multiply them together to get the power rating."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with diagnostic data.")

    args = parser.parse_args()

    ###########################################################################
    # Read in directions
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            diagnostic_data = [value.strip() for value in FILE.readlines()]
    except Exception:
        raise

    ###########################################################################
    # Interpret diagnostic data
    ###########################################################################

    # Check if there is enough data
    if len(diagnostic_data) < 1:
        print("Not enough diagnostic data to determine gamma and epsilon rates.")
        exit(1)

    # Initialize a bit counter. Each bit starts at 0. If a "1" is read, increment
    # the bit counter by 1. If a "0" is read, decrement the bit counter by 1.
    #
    # This method is used because the data is read in from the files as rows of
    # data. The gamma and epsilon rates are determined by columns of data. This
    # method will aggregate the column values (gamma and epsilon rates) by
    # reading each row.
    bit_counter = [0] * len(diagnostic_data[0])

    # Read each line of diagnostic data
    for line_number, bits in enumerate(diagnostic_data, 1):
        # Read each bit
        for index, bit in enumerate(bits):
            # Bit value is 1
            if bit == "1":
                bit_counter[index] += 1
            # Bit value is 0
            elif bit == "0":
                bit_counter[index] -= 1
            # Invalid bit value
            else:
                print("ERROR: Invalid bit value found on line number {} bit number {}.".format(line_number, index+1))

    ###########################################################################
    # Determine gamma and epsilon rates
    ###########################################################################

    # Binary strings of the gamma and epsilon rates
    gamma_rate_bin_str = ""
    epsilon_rate_bin_str = ""

    # Read each bit count and determine if a 1 or 0 should be added to the gamma
    # and epsilon rates
    for bit_position, bit_count in enumerate(bit_counter):
        # Gamma gets a 1; epsilon gets a 0
        if bit_count > 0:
            gamma_rate_bin_str += "1"
            epsilon_rate_bin_str += "0"
        # Gamma gets a 0; epsilon gets a 1
        elif bit_count < 0:
            gamma_rate_bin_str += "0"
            epsilon_rate_bin_str += "1"
        # Even number of 0s and 1s found
        else:
            print("ERROR: Equal number of 1s and 0s found in bit position {}.".format(bit_position))
            exit(2)

    ###########################################################################
    # Report
    ###########################################################################

    gamma_rate = int(gamma_rate_bin_str, 2)
    epsilon_rate = int(epsilon_rate_bin_str, 2)

    print("Gamma rate:        {}".format(gamma_rate))
    print("Epsilon rate:      {}".format(epsilon_rate))
    print("Power consumption: {}".format(gamma_rate * epsilon_rate))

    exit(0)


if __name__ == '__main__':
    main()
