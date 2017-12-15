def find_unvisited_edge(G, node, visited):
    """Return the first unvisited edge from a given node using the visited set."""
    for neighbor in G[node].keys():
        edge = (min(node, neighbor), max(node, neighbor))
        if edge not in visited:
            return edge
    return None


def euler(G, origin=None):
    """Use Hierholzer's algorithm to find an Euler circuit of an undirected graph."""
    # Check whether the graph is eulerian or semi-eulerian
    if G.is_eulerian():
        eulerian = True
    elif G.is_semi_eulerian():
        eulerian = False
    else:
        raise Exception("Graph needs to be eulerian or semi-eulerian")

    visited = set()  # Keep track of visited edges
    tour = []  # Will hold the final eulerian tour
    subtour = []

    if eulerian:
        # Any vertex can be a starting point
        if origin is None:
            origin = destiny = G.nodes()[0]
        else:
            assert origin in G.nodes(), "The origin node is not in the graph"
            destiny = origin
    else:
        # The path must start and end on the nodes with odd degree
        odd_nodes = [node for node in G.nodes() if G.degree(node) % 2 != 0]
        if origin is None:
            origin, destiny = odd_nodes
        else:
            assert origin in odd_nodes, "Graph is semi-eulerian, origin must be node of odd degree"
            odd_nodes.remove(origin)
            destiny = odd_nodes[0]

    subtour.append(origin)
    current = origin

    while subtour:
        # Get an unvisited edge from the current node, which we know must exist
        edge = find_unvisited_edge(G, current, visited)
        visited.add(edge)
        print(edge)
        neighbor = edge[1] if edge[0] == current else edge[0]
        subtour.append(neighbor)

        # Check if we have completed a loop
        if neighbor == origin or neighbor == destiny:
            # Integrate subtour into final tour until we find unvisited edges
            while subtour:
                prev = subtour.pop()
                unvisited_edge = find_unvisited_edge(G, prev, visited)
                if unvisited_edge:
                    # Unvisited edge found, keep executing algorithm with new origin
                    subtour.append(prev)
                    current = origin = prev
                    break
                tour.append(prev)

        else:
            current = neighbor

    return list(reversed(tour))
