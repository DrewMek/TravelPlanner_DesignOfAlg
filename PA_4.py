from collections import deque

# loading flight data and building graph
def load_flights(filename):
    graph = {}

    # Read the flight data and build the graph
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Process each line to build the graph
    for i in range(len(lines)):
        line = lines[i].strip()

        # Ensure the line is in the correct format for eval
        if not line.startswith('['):
            line = '[' + line
        
        # Ensure the line ends with a closing bracket
        if not line.endswith(']'):
            line = line + ']'

        # Safely evaluate the line to get the list of edges
        edges = eval(line)

        # Extract neighbors for the current city
        neighbors = []

        # Each edge is a tuple (destination, distance), we only care about the destination
        for edge in edges:
            dest = edge[0]
            neighbors.append(dest)

        # Store the neighbors in the graph
        graph[i + 1] = neighbors  

    return graph


# BFS 
def bfs_all_paths(graph, start):

    #queue for BFS
    queue = deque()
    queue.append(start)

    # Set to track visited cities
    visited = set()
    visited.add(start)

    parent = {}

    # BFS loop
    while queue:
        current = queue.popleft()

        # Explore neighbors
        for neighbor in graph[current]:

            # If neighbor hasn't been visited, add to queue and mark parent
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return parent


# Making path from start to end using parent mapping
def get_path(parent, start, end):

    #path reconstruction
    path = []
    node = end

    # Backtrack from end to start using parent mapping
    while node != start:
        path.append(node)
        node = parent[node]

    # Finally add the start node
    path.append(start)
    path.reverse()

    return tuple(path)


# MAIN COMPUTATION: BFS for each city to find min stops to all others
def compute_all_min_stops(graph):
    result = []

    # BFS for each city
    for i in range(1, 101):
        parent = bfs_all_paths(graph, i)  # ONE BFS per i
        row = []

        # reconstruct paths to all other cities
        for j in range(1, 101):
            if i != j:
                path = get_path(parent, i, j)
                row.append(path)

        result.append(row)

    return result


# Output function
def write_output(data, filename):

    # Write the paths to the output file in the specified format
    with open(filename, 'w') as f:

        # Write each row of paths to the file
        for row in data:
            line = []

            # Format each path in the row
            for path in row:

                # Format the path as required
                line.append("(" + " -> ".join(map(str, path)) + ")")

            # Write the line to the file
            f.write(", ".join(line) + "\n")


# Main execution

# Load graph from flights.txt
graph = load_flights("flights.txt")

# Compute all minimum stop paths
data = compute_all_min_stops(graph)

# Write output to file
write_output(data, "minstops.txt")