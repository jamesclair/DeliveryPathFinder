def dijkstra_shortest_path(graph, start_location):
    unvisited_queue = []
    for v in graph.adjacency_list:
        unvisited_queue.append(v)

    start_location.distance = 0

    while len(unvisited_queue) > 0:
        smallest = 0

        for e in range(1, len(unvisited_queue)):
            if unvisited_queue[e].distance < unvisited_queue[smallest].distance:
                smallest = e

        current_location = unvisited_queue.pop(smallest)

        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in graph.adjacency_list[current_location]:
            # print("current_location.label: ", current_location.label)
            # print("current_location.distance: ", current_location.distance)
            # print("current_location.predecessor: ", current_location.predecessor)
            # print("adj_vertex.label: ", adj_vertex.label)
            # print("adj_vertex.distance: ", adj_vertex.distance)
            # print("adj_vertex.predecessor: ", adj_vertex.predecessor)

            edge_weight = graph.edge_weights[(current_location, adj_vertex)]
            # print("edge_weight: ", edge_weight)
            alternative_path_distance = current_location.distance + edge_weight
            # print("alternative_path: ", alternative_path_distance)
            # If shorter path from start_location to adj_vertex is found,
            # update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                # print("updating adj vertex distance to: ", alternative_path_distance)
                adj_vertex.distance = alternative_path_distance
                adj_vertex.predecessor = current_location
            # else:
                # print("did not update adj vertex distance")


def get_shortest_path(start_location, end_location):
    # Start from end_vertex and build the path backwards.
    path = []
    current_location = end_location
    # print("current_location_type: ", type(current_location))
    # print("current_location_label: ", current_location.label)
    # print("start_location_type: ", type(start_location))
    # print("start_location_label: ", start_location.label)
    # print("----Starting while loop----")
    while current_location is not start_location:
        if current_location.predecessor is None:
            break
        print("current_location_type: ", type(current_location))
        print("current_location_label: ", current_location.label)
        print("start_location_type: ", type(start_location))
        print("start_location_label: ", start_location.label)
        print("current_location_predecessor: ", current_location.predecessor)
        print("current_location_predecessor_type: ", type(current_location.predecessor))
        print(current_location.label)
        path.insert(0, current_location)
        path = " -> " + str(current_location.label) + path
        current_location = current_location.predecessor
    path.insert(0, start_location)
    path = start_location.label + path
    return path
