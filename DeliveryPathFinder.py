# James Clair, 000847594

import LoadData
import Model
import ShortestPath


def main():
    package_list = LoadData.load_packages()
    distance_graph = LoadData.load_distances()

    ShortestPath.dijkstra_shortest_path(distance_graph, distance_graph.hub_vertex)

    hub = Model.Hub()
    truck_1 = Model.Truck(1, hub.drivers[0])
    truck_2 = Model.Truck(2, hub.drivers[1])
    truck_3 = Model.Truck(3)  # Driver assigned once first truck returns.

    # Sort packages by distance
    sorted_packages = []
    visited = []

    packages_by_address = hub.get_packages_by_address(package_list)
    start_v = distance_graph.hub_vertex

    closest_v = distance_graph.hub_vertex
    visited.append(closest_v)

    # for v in distance_graph.adjacency_list:
    #
    #     if v.label not in packages_by_address:
    #         print(v.label)
    for v1 in distance_graph.adjacency_list:
        for v2 in distance_graph.adjacency_list[v1]:
            closest_distance = float('inf')
            if v2 not in visited and v2.distance < closest_distance:
                closest_v = v2
        visited.append(closest_v)

        for package in packages_by_address[closest_v.label]:
            sorted_packages.append(package)

    # Load packages with special notes
    for package in sorted_packages:
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

    # Load the rest of packages
    for package in sorted_packages:
        if package.delivery_status != 'loaded':
            print(package.package_id, ": ", package.delivery_status)
            if truck_1.load_on_truck(package):
                break
            elif truck_2.load_on_truck(package):
                break
            elif truck_3.load_on_truck(package):
                break
            else:
                print("All trucks are full your hub is overloaded.  Better get that checked out.")
    print('All trucks are loaded')

    # Deliver packages
    total_distance = 0
    start_v = distance_graph.hub_vertex

    list_of_trucks = [truck_1, truck_2, truck_3]
    for truck in list_of_trucks:

        if truck.truck_id in [1, 2]:
            current_time = hub.start_time
        else:
            if truck_1.finish_time < truck_2.finish_time:
                current_time = truck_1.finish_time
            else:
                current_time = truck_2.finish_time
        print('')
        print('Truck {0} start time: {1}'.format(truck.truck_id, current_time))

        packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
        for package in truck.delivery_queue:
            if package is None:
                continue
            else:
                for v in distance_graph.adjacency_list[start_v]:
                    if v.label == package.delivery_address:
                        truck.distance = truck.distance + v.distance
                        total_distance = total_distance + v.distance
                        print('Path from {0}, to {1}: \n{2}\nDistance = {3}'.format(start_v, v,
                                                                                    ShortestPath.get_shortest_path(
                                                                                        start_v, v), v.distance))
                        for other_package in packages_by_address[v.label]:
                            other_package.delivery_time = (v.distance / 8)
                            other_package.delivery_status = 'delivered'

                        current_time = current_time + package.delivery_time
                        print('The following packages took {0} to deliver and arrived at {1}:'.format(
                            package.delivery_time,
                            current_time))

                        print(package)
                        print('')
        truck.finish_time = current_time
        print('Truck {0}, driver {1} delivered all'
              ' packages at {2} and traveled {3} miles.'.format(truck.truck_id, truck.driver, current_time,
                                                                truck.distance))
        print('')

    print('Total distance of all trucks: ', total_distance)


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
