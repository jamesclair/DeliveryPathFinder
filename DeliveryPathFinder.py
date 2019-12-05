# James Clair, 000847594

import Model
import LoadData
import ShortestPath


def main():
    package_list = LoadData.load_packages()
    distance_graph = LoadData.load_distances()

    for v in distance_graph.adjacency_list:
        ShortestPath.dijkstra_shortest_path(distance_graph, distance_graph.hub_vertex)

    hub = Model.Hub()
    truck_1 = Model.Truck(1, hub.drivers[0])
    truck_2 = Model.Truck(2, hub.drivers[1])
    truck_3 = Model.Truck(3)

    # Load trucks
    for package in package_list:
        # Sort packages with special notes
        if package.special_note != "":
            note_parts = package.special_note.split(' ')
            if note_parts[0] == "Delayed":
                truck_3.load_on_truck(package)
            elif note_parts[-2] == 'truck':
                if note_parts[-1] == '1':
                    truck_1.load_on_truck(package)
                elif note_parts[-1] == '2':
                    truck_2.load_on_truck(package)
                elif note_parts[-1] == '3':
                    truck_3.load_on_truck(package)
            elif note_parts[0] == "Wrong":
                package.is_wrong_addr = True
            else:
                package.peer_packages.append(note_parts[-2][:-1])
                package.peer_packages.append(note_parts[-1])
                truck_1.load_on_truck(package)
                for p in package.peer_packages:
                    p = int(p)
                    if not package_list[p - 1].delivery_status == 'loaded':
                        truck_1.load_on_truck(package_list[p - 1])

    # Loading the rest of the packages on the trucks grouped by their zip codes
    # With the proper state management there would be no need to iterate the over the full list again.
    packages_by_address = hub.get_packages_by_address(package_list)
    for address in packages_by_address.keys:
        for package in packages_by_address.read(address):
            if package.status != 'loaded':
                if truck_1.load_on_truck(package):
                    return
                elif truck_2.load_on_truck(package):
                    return
                elif truck_3.load_on_truck(package):
                    return
                else:
                    print("All trucks are full your hub is overloaded.  Better get that checked out.")
    print('All trucks are loaded')

    current_time = time()
    current_address = 'hub'
    distance = 0
    ctime(current_time)

    # for package in truck_1.delivery_queue:
    #     if package is not None:
    #         print("truck 1: ", package)
    #
    # for package in truck_2.delivery_queue:
    #     if package is not None:
    #         print("truck 2: ", package)
    #
    # if truck_1.finish_time < truck_2.finish_time:
    #     current_time = truck_1.finish_time
    # else:
    #     current_time = truck_2.finish_time
    #
    # for package in truck_3.delivery_queue:
    #     if package is not None:
    #         print("truck 3: ", package)
    #
    # # Deliver packages based on smallest distance
    # closest_v = int('inf')
    # for v in distance_graph.adjacency_list[distance_graph.hub_vertex]:
    #     if v.distance < closest_v:
    #         closest_v = v
    #
    # packages_by_address = hub.get_packages_by_address(truck_1.delivery_queue)
    # for package in packages_by_address[closest_v.label]:
    #     if package is None:
    #         print('package is None\n')
    #         break
    #     else:
    #         package.delivery_time = time()
    #         package.delivery_status='delivered'
    #
    #
    # for v1 in distance_graph.adjacency_list:
    #     for v2 in distance_graph.adjacency_list[v1]:
    #         print('Path from {0}, to {1}: \n{2}\nDistance = {3}'.format(v1, v2, ShortestPath.get_shortest_path(v1, v2), v2.distance))


# TODO: per truck name, driver, Departure, Arrival, print # of miles
#  Per package Print # of miles, package deadline, and time package arrived
# TODO: Print # of total miles and delivery finish

# TODO: Provide an interface for the insert and look-up functions to view the status of any package at any time. This function should return all information about each package, including delivery status.
# 		1.  Provide screenshots to show package status of all packages at a time between 8:35 a.m. and 9:25 a.m.
# 		2.  Provide screenshots to show package status of all packages at a time between 9:35 a.m. and 10:25 a.m.
#       3.  Provide screenshots to show package status of all packages at a time between 12:03 p.m. and 1:12 p.m.
# TODO: Example of looking up package status at some point in the time line
# TODO: The wrong delivery address for package #9, Third District Juvenile Court, will be corrected at 10:20 a.m. The correct address is 410 S State St., Salt Lake City, UT 84111.


#  Unit Tests:
# tests.ModelTests.test_truck()
# tests.ModelTests.test_package()
# tests.ModelTests.test_hashtable()


if __name__ == "__main__":
    main()
