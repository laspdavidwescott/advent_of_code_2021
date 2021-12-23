#!/usr/bin/env python3

import argparse
import sys
import datetime


def expand_map(risk_level_map, expansion_factor=5):
    """ Algorithmically expand the given risk level map by the given expansion
        factor. For each row and/or column, add 1 to each risk value. If a risk
        value is 9, it becomes 1.

        Input:  risk level map [[risk level <int>]]
                expansion factor <int>

        Output: expanded risk level map [[risk level <int>]]
    """
    # The returned expanded map
    expanded_map = []

    # The given map's row and column counts
    risk_level_row_count = len(risk_level_map)
    risk_level_column_count = len(risk_level_map[0]) if risk_level_row_count > 0 else 0

    # Build the expanded map one row at a time
    for row in range(risk_level_row_count * expansion_factor):
        # A row in the expanded map
        expanded_row = []

        # Translate the expanded map row to the given map row
        risk_level_row = row % risk_level_row_count

        # Each column of the expanded map
        for column in range(risk_level_column_count * expansion_factor):
            # Translate the expanded map column to the given map column
            risk_level_column = column % risk_level_column_count

            # Calculate the risk for this row and column in the expanded map
            risk = risk_level_map[risk_level_row][risk_level_column]
            risk += row // risk_level_row_count + column // risk_level_column_count

            # Roll over if the risk is too high
            if risk > 9:
                risk %= 9

            # Append the calculated risk
            expanded_row.append(risk)

        # Append the expanded row to the expanded map
        expanded_map.append(expanded_row)

    return expanded_map


def get_least_risky_vertex(vertex_risks):
    """ Return the vertex with the least risk to the starting vertex.

        Input:  vertex risks { vertex (row <int>, column <int>) : risk <int> }

        Output: unvisited vertex with least risk (row <int>, column <int>)
    """
    # Keep track of the least risky vertex and its risk
    least_risky_vertex = (None, None)
    least_risk = sys.maxsize

    # Check each vertex and corresponding disk
    for vertex, risk in vertex_risks.items():
        # Check if this is the new least risky
        if risk < least_risk:
            least_risky_vertex = vertex
            least_risk = risk

    # Return the least risky vertex
    return least_risky_vertex


def get_vertex_neighbors(vertex, row_count, column_count, vertices_visited):
    """ Return the unvisited neighbors of the given vertex.

        Input:  vertex (row <int>, column <int>)
                vertices_visited {vertex (row <int>, column <int>)}

        Output: vertex neighbors [vertex (row <int>, column <int>)]
    """
    # The given vertex's row and column
    row, column = vertex

    # Neighboring vertices
    north = (row - 1, column) if 0 <= row - 1 else None
    east = (row, column + 1) if column + 1 < column_count else None
    south = (row + 1, column) if row + 1 < row_count else None
    west = (row, column - 1) if 0 <= column - 1 else None

    neighbor_vertices = (north, east, south, west)

    # Return valid unvisited neighbor vertices
    return [neighbor_vertex for neighbor_vertex in neighbor_vertices if neighbor_vertex is not None and neighbor_vertex not in vertices_visited]


def main():
    """ Read in the chiton risk level map provided by the given file.
        Increase the map size algorithmically. Find the path from the
        top left to the bottom right with the lowest total risk.
    """
    start_time = datetime.datetime.now()

    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the chiton risk level map provided by the given file.\n" \
                  "Increase the map size algorithmically. Find the path from the\n" \
                  "top left to the bottom right with the lowest total risk."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with chiton risk level map.")
    parser.add_argument("--debug", action='store_true', help="Enable debug")
    parser.add_argument("--start-row", type=int, help="Starting vertex row", default=0)
    parser.add_argument("--start-column", type=int, help="Starting vertex column", default=0)
    parser.add_argument("--end-row", type=int, help="Starting vertex row", default=None)
    parser.add_argument("--end-column", type=int, help="Starting vertex column", default=None)
    parser.add_argument("-e", "--expansion-factor", type=int, help="Multiply the risk level map size by this amount", default=5)

    args = parser.parse_args()

    ###########################################################################
    # Read in lines of syntax
    ###########################################################################

    try:
        with open(args.file, 'r') as FILE:
            risk_level_data = [value.strip() for value in FILE.readlines()]
    except Exception:
        raise

    # Make sure there is data
    if len(risk_level_data) == 0:
        print("Risk level map not found in {}".format(args.file))
        exit(1)

    ###########################################################################
    # Initialize and verify map
    ###########################################################################

    # The map [[risk level <int>]]
    risk_level_map = [list(map(int, list(risk_levels))) for risk_levels in risk_level_data]

    # Expand the map algorithmically
    risk_level_map = expand_map(risk_level_map, expansion_factor=args.expansion_factor)

    if args.debug:
        print("Expanded risk level map")

        for risk_level_row in risk_level_map:
            print(risk_level_row)

        print()

    # Get the map's row and column counts
    row_count = len(risk_level_map)
    column_count = len(risk_level_map[0]) if 0 < row_count else 0

    # Get the starting vertex (row and column)
    start_row = args.start_row
    start_column = args.start_column

    # Get the ending vertex (row and column)
    end_row = row_count - 1 if args.end_row is None else args.end_row
    end_column = column_count - 1 if args.end_column is None else args.end_column

    # Check if the given row and column are in the map
    if row_count <= start_row or start_row < 0 or column_count <= start_column or start_column < 0:
        print("ERROR: Given starting row '{}' and column '{}' fall outside the given map.".format(start_row, start_column))
        exit(1)

    # Check if the given row and column are in the map
    if row_count <= end_row or end_row < 0 or column_count <= end_column or end_column < 0:
        print("ERROR: Given ending row '{}' and column '{}' fall outside the given map.".format(end_row, end_column))
        exit(1)

    ###########################################################################
    # Calculate the vertex risks from the starting vertex
    ###########################################################################

    # Initialize a matrix (2D list) of all the vertex's risks and previous
    # vertices. Set the starting vertex's risk to 0.
    risks_and_previous_vertices = [[[sys.maxsize, tuple([None, None])] for _ in range(len(risk_level_row))] for risk_level_row in risk_level_map]
    risks_and_previous_vertices[start_row][start_column][0] = 0

    # Total number of vertices
    vertex_count = row_count * column_count

    # Keep track of the visited vertices
    vertices_visited = set()

    # Keep track least risky vertex candidates
    least_risky_vertex_candidates = {(start_row, start_column): 0}

    # While there are vertices to visit
    while len(vertices_visited) < vertex_count:
        if args.debug:
            start_vertex_time = datetime.datetime.now()

        # Get the least risky vertex that hasn't been visited (current vertex)
        current_vertex = get_least_risky_vertex(least_risky_vertex_candidates)
        current_row, current_column = current_vertex

        if args.debug:
            print("Current Vertex: {}".format(current_vertex))

        # Get the current vertex's unvisited neighboring vertices
        neighbor_vertices = get_vertex_neighbors(current_vertex, row_count, column_count, vertices_visited)

        # Check each neighboring vertex
        for neighbor_vertex in neighbor_vertices:
            # Split the vertex up into row and column
            neighbor_row, neighbor_column = neighbor_vertex

            # Calculate the risk from start to this vertex
            risk = risks_and_previous_vertices[current_row][current_column][0] + risk_level_map[neighbor_row][neighbor_column]

            if args.debug:
                print("    Neighbor Vertex: {} --> {}".format(neighbor_vertex, risk))

            # If the calculated (above) risk is less than the saved risk
            if risk < risks_and_previous_vertices[neighbor_row][neighbor_column][0]:
                # Update the neighbor's risk and "previous" vertex
                risks_and_previous_vertices[neighbor_row][neighbor_column][0] = risk
                risks_and_previous_vertices[neighbor_row][neighbor_column][1] = current_vertex

                # Update the least risky vertex candidates
                least_risky_vertex_candidates[(neighbor_row, neighbor_column)] = risk

        # Mark the vertex as visited
        vertices_visited.add(current_vertex)

        # Remove the vertex from the least risky vertex candidates (since it's
        # been visited)
        del least_risky_vertex_candidates[current_vertex]

        if args.debug:
            print("    Vertex time: {}".format(datetime.datetime.now() - start_vertex_time))

    if args.debug:
        print()

    ###########################################################################
    # Report
    ###########################################################################

    total_risk = risks_and_previous_vertices[end_row][end_column][0]
    start_vertex = (start_row, start_column)
    end_vertex = (end_row, end_column)

    print("The total risk to go from {} to {} is {}".format(start_vertex, end_vertex, total_risk))
    print("Elapsed Time: {}".format(datetime.datetime.now() - start_time))


if __name__ == '__main__':
    main()
