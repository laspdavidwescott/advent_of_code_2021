#!/usr/bin/env python3

import argparse


def filter_data(dataset, bit_index, bit_value):
    """ Filter the given dataset. Keep all the values that have the given bit
        value at the given bit index. Discard all others.

        Return the filtered dataset.

        Input:  data [ binary value <str> ]
                bit index <int>
                bit value <int>

        Output: filtered dataset [ binary value <str> ]
    """
    # The value will be compared as a string
    bit_value = str(bit_value)

    # The returned filtered dataset
    filtered_dataset = []

    # Check each binary value (string)
    for binary_value in dataset:
        # If the bit matches the given bit value, add the binary value to the
        # returned dataset
        if binary_value[bit_index] == bit_value:
            filtered_dataset.append(binary_value)

    return filtered_dataset


def find_most_least_common_bits(dataset):
    """ Find the most and least common bits in the given dataset. The dataset
        if a list of a binary strings. Each binary value needs to be the same
        length (precision).

        A list of bit counts is returned. If the bit count is positive, 1 was
        the most common bit. If the bit count is negative, 0 was the most
        common bit. If the bit count is zero, then an even number of 1s and 0s
        were found.

        Input:  data [ binary value <str> ]

        Output: most and least common bits [ count <int> ]
    """
    # Initialize a bit counter. Each bit starts at 0. If a "1" is read, increment
    # the bit counter by 1. If a "0" is read, decrement the bit counter by 1.
    bit_counter = [0] * len(dataset[0])

    # Read each line of diagnostic data
    for line_number, bits in enumerate(dataset, 1):
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
                print("ERROR: Invalid bit value found on line number {} bit number {}.".format(line_number, index + 1))

    return bit_counter


def get_co2_scrubber_rating(dataset):
    """ Determine the CO2 scrubber rating from the given dataset.

        Input:  binary dataset [ binary value <str>]

        Output: CO2 scrubber rating <int>
    """
    # Make a copy of the dataset so we don't destroy original list
    _dataset = [value for value in dataset]

    # Loop until an answer is found or run out of bits
    for bit_index in range(len(_dataset[0])):
        # Find the bit counts of the current dataset
        bit_counts = find_most_least_common_bits(_dataset)

        # Determine the bit value (0 or 1) for the current bit index
        bit_value = 1 if bit_counts[bit_index] < 0 else 0

        # Filter the binary value dataset
        _dataset = filter_data(_dataset, bit_index, bit_value)

        # If a single value is left in the dataset, stop
        if len(_dataset) == 1:
            break
    # Could not find the rating
    else:
        print("ERROR: Failed to find CO2 scrubber rating.")
        return -1

    # Convert the rating to an integer
    co2_scrubber_rating = int(_dataset[0], 2)

    return co2_scrubber_rating


def get_oxygen_generator_rating(dataset):
    """ Determine the oxygen generator rating from the given dataset.

        Input:  binary dataset [ binary value <str>]

        Output: oxygen generator rating <int>
    """
    # Make a copy of the dataset so we don't destroy original list
    _dataset = [value for value in dataset]

    # Loop until an answer is found or run out of bits
    for bit_index in range(len(_dataset[0])):
        # Find the bit counts of the current dataset
        bit_counts = find_most_least_common_bits(_dataset)

        # Determine the bit value (0 or 1) for the current bit index
        bit_value = 1 if bit_counts[bit_index] >= 0 else 0

        # Filter the binary value dataset
        _dataset = filter_data(_dataset, bit_index, bit_value)

        # If a single value is left in the dataset, stop
        if len(_dataset) == 1:
            break
    # Could not find the rating
    else:
        print("ERROR: Failed to find oxygen generator rating.")
        return -1

    # Convert the rating to an integer
    oxygen_generator_rating = int(_dataset[0], 2)

    return oxygen_generator_rating


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

    # Get the oxygen generator and CO2 scrubber ratings
    oxygen_generator_rating = get_oxygen_generator_rating(diagnostic_data)
    co2_scrubber_rating = get_co2_scrubber_rating(diagnostic_data)

    ###########################################################################
    # Report
    ###########################################################################

    print("Submarine oxygen generator rating: {}".format(oxygen_generator_rating))
    print("Submarine CO2 scrubber rating:     {}".format(co2_scrubber_rating))
    print("Life support rating:               {}".format(oxygen_generator_rating * co2_scrubber_rating))

    # Figure out the return code and exit
    return_code = 1 if oxygen_generator_rating < 0 or co2_scrubber_rating < 0 else 0
    exit(return_code)


if __name__ == '__main__':
    main()
