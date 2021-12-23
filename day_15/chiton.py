#!/usr/bin/env python3

import argparse
import sys
import datetime


def get_smallest_distance_vertex(vertex_values, vertices_visited):
    """ Return the vertex with the smallest distance to the starting vertex
        that has not been visited.

        Input:  vertex values [[[distance <int>, previous vertex (row <int> column <int>)]]]
                vertices visited {(row <int>, column <int>)}

        Output: unvisited vertex with smallest distance (row <int>, column <int>)
    """
    # Keep track of the smallest vertex and its distance from the starting
    # vertex
    smallest_vertex = (None, None)
    smallest_distance = sys.maxsize

    # Check each distance
    for row in range(len(vertex_values)):
        for column in range(len(vertex_values[row])):
            # Get the vertex and distance
            vertex = (row, column)
            distance = vertex_values[row][column][0]

            # If the distance is smaller than the previous distance and the
            # vertex hasn't been visited yet, save this vertex and distance
            if distance < smallest_distance and vertex not in vertices_visited:
                smallest_distance = distance
                smallest_vertex = vertex

    # Return the smallest vertex
    return smallest_vertex


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
        Find the path from the top left to the bottom right with the lowest
        total risk.
    """
    start_time = datetime.datetime.now()

    ###########################################################################
    # Command line argument parser
    ###########################################################################

    description = "Read in the chiton risk level map provided by the given file.\n" \
                  "Find the path from the top left to the bottom right with the lowest\n" \
                  "total risk."

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Text file with chiton risk level map.")
    parser.add_argument("--debug", action='store_true', help="Enable debug")
    parser.add_argument("--start-row", type=int, help="Starting vertex row", default=0)
    parser.add_argument("--start-column", type=int, help="Starting vertex column", default=0)
    parser.add_argument("--end-row", type=int, help="Starting vertex row", default=None)
    parser.add_argument("--end-column", type=int, help="Starting vertex column", default=None)

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

    # The graph [[risk level <int>]]
    risk_level_graph = [list(map(int, list(risk_levels))) for risk_levels in risk_level_data]

    row_count = len(risk_level_data)
    column_count = len(risk_level_data[0]) if 0 < row_count else 0

    start_row = args.start_row
    start_column = args.start_column

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

    vertex_values = [[[sys.maxsize, tuple([None, None])] for _ in range(len(risk_level_row))] for risk_level_row in risk_level_graph]
    vertex_values[start_row][start_column][0] = 0

    row_count = len(vertex_values)
    column_count = len(vertex_values[0])
    vertex_count = row_count * column_count

    vertices_visited = set()

    print("Before while: {}".format(datetime.datetime.now() - start_time))

    while len(vertices_visited) < vertex_count:
        start_vertex_time = datetime.datetime.now()

        current_vertex = get_smallest_distance_vertex(vertex_values, vertices_visited)
        row, column = current_vertex

        if args.debug:
            print("Current Vertex: {}".format(current_vertex))

        neighbor_vertices = get_vertex_neighbors(current_vertex, row_count, column_count, vertices_visited)

        for neighbor_vertex in neighbor_vertices:
            neighbor_row, neighbor_column = neighbor_vertex
            distance = vertex_values[row][column][0] + risk_level_graph[neighbor_row][neighbor_column]

            if args.debug:
                print("    Neighbor Vertex: {} --> {}".format(neighbor_vertex, distance))

            if distance < vertex_values[neighbor_row][neighbor_column][0]:
                vertex_values[neighbor_row][neighbor_column][0] = distance
                vertex_values[neighbor_row][neighbor_column][1] = current_vertex

        vertices_visited.add(current_vertex)

        print("    Vertex time: {}".format(datetime.datetime.now() - start_vertex_time))

    if args.debug:
        print()

    total_risk = vertex_values[end_row][end_column][0]
    start_vertex = (start_row, start_column)
    end_vertex = (end_row, end_column)
    print("The total risk to go from {} to {} is {}".format(start_vertex, end_vertex, total_risk))
    print("Elapsed Time: {}".format(datetime.datetime.now() - start_time))


if __name__ == '__main__':
    main()
