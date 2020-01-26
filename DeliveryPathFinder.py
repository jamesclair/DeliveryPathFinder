# James Clair, 000847594
import copy
import datetime

import LoadData
import Model
import ShortestPath


def get_formatted_time(time):
    hh = int(time)
    mm = (time * 60) % 60
    ss = (time * 3600) % 60
    return "%d:%02d:%02d" % (hh, mm, ss)


def get_hours_float(time):
    times = []

    for x in time.split(':'):
        times.append(int(x))

    time = datetime.time(times[0], times[1], times[2])
    return float(time.hour + time.minute / 60 + time.second / 3600)


def find_closest_location(delivery_queue):
    closest_distance = float('inf')
    smallest = None
    for i in range(0, len(delivery_queue) - 1):
        print('location:', delivery_queue[i].location.label)
        print('distance:', delivery_queue[i].location.distance)
        if delivery_queue[i].location.distance < closest_distance and delivery_queue[i].location.distance is not 0:
            smallest = i
    if smallest is not None:
        return delivery_queue[smallest].location
    else:
        return None


# def check_status(current_time, package_list, hub):
#     packages_by_status = hub.get_packages_by_status(package_list)
#     if ((get_hours_float('8:35:00') <= current_time <= get_hours_float('9:25:00') and hub.count == 0) or (
#             get_hours_float('9:35:00') <= current_time <= get_hours_float('10:25:00') and hub.count == 1) or (
#             get_hours_float('12:03:00') <= current_time <= get_hours_float('13:12:00') and hub.count == 2)):
#         print('*** {0} Status Check ***'.format(get_formatted_time(current_time)))
#         hub.count = hub.count + 1


def deliver_package(package, time):
    package.arrival_time = time
    package.delivery_status = 'delivered'


def main():
    package_list = LoadData.load_packages()
    distance_graph = LoadData.load_distances()

    hub = Model.Hub()
    truck_1 = Model.Truck(1, hub.drivers[0])
    truck_2 = Model.Truck(2, hub.drivers[1])
    truck_3 = Model.Truck(3)  # Driver assigned once first truck returns.
    trucks = [truck_1, truck_2, truck_3]

    # Load packages with special notes
    original_list = package_list.copy()
    for package in original_list:
        # Sort packages with special notes
        if package.special_note != "":
            package.delivery_status = 'loaded'
            note_parts = package.special_note.split(' ')
            print(note_parts[0])
            if note_parts[0] == "Delayed" or note_parts[0] == "Wrong":
                if truck_3.load_on_truck(package):
                    package_list.remove(package)
            elif note_parts[-2] == 'truck':
                if note_parts[-1] == '1':
                    if truck_1.load_on_truck(package):
                        package_list.remove(package)
                elif note_parts[-1] == '2':
                    if truck_2.load_on_truck(package):
                        package_list.remove(package)
                elif note_parts[-1] == '3':
                    if truck_3.load_on_truck(package):
                        package_list.remove(package)
            else:
                # print(note_parts[0])
                package.peer_packages.append(note_parts[-2][:-1])
                package.peer_packages.append(note_parts[-1])
                if truck_1.load_on_truck(package):
                    package_list.remove(package)
                # print('Peer packages for {0} are: '.format(package.delivery_address))
                # for e in package.peer_packages:
                # print(e)
                for p2 in package_list:
                    if p2.package_id in package.peer_packages and p2.delivery_status != 'loaded':
                        if truck_1.load_on_truck(p2):
                            package_list.remove(p2)

    # find shortest path to hub
    for package in package_list:
        if truck_1.load_on_truck(package):
            continue
        elif truck_2.load_on_truck(package):
            continue
        elif truck_3.load_on_truck(package):
            continue
        else:
            print('Unable to load package on truck')

    for truck in trucks:
        print('#' * 118)
        print('# Truck {0}:'.format(truck.truck_id))
        print('# Truck {0} delivery queue length: {1}'.format(truck.truck_id, len(truck.delivery_queue)))
        print('#' * 118)
        for package in truck.delivery_queue:
            print(package)

    # Deliver packages
    last_location = distance_graph.hub_vertex
    for truck in trucks:
        # set the current time
        ShortestPath.dijkstra_shortest_path(distance_graph, last_location)
        truck.start_time = hub.start_time
        if truck.truck_id == 3:
            truck.start_time = min(truck_1.start_time, truck_2.start_time)
        print('# Truck {0} start: {1}'.format(truck.truck_id, truck.start_time))
        current_time = truck.start_time

        # first location
        current_location = find_closest_location(truck.delivery_queue)
        print('First location:', current_location.label)

        # Deliveries
        count = 0
        last_location = distance_graph.hub_vertex
        while len(truck.delivery_queue) > 0:
            # Deliver packages for location
            print('last_total: {0} '.format(hub.total_distance), end='')
            print('+ distance from last: {0} = '.format(current_location.distance), end='')
            hub.total_distance += current_location.distance
            print('new_total: {0}'.format(hub.total_distance))

            print('last_truck_distance: {0} '.format(truck.distance), end='')
            print('+ distance from last: {0} = '.format(current_location.distance), end='')
            truck.distance += current_location.distance
            print('new_truck_distance: {0}'.format(truck.distance))
            current_time += (current_location.distance / 18)

            packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
            for package in packages_by_address[current_location.label]:
                deliver_package(package, current_time)
                truck.delivery_queue.remove(package)
                print(package)

            # Update truck's path
            # print('last_location:', last_location.label)
            # print('current_location:', current_location.label)
            # print('running shortest path')
            # truck.paths.append(ShortestPath.get_shortest_path(last_location, current_location))

            last_location = current_location
            # Run dijkstras
            print(last_location.distance)
            # TODO: Figure out why vertices are setting their distance to 0 and if you need to set their distances to float('inf') before running dijkstras
            ShortestPath.dijkstra_shortest_path(distance_graph, current_location)

            # Update next location
            current_location = find_closest_location(truck.delivery_queue)
            if current_location is None:
                break
        ShortestPath.dijkstra_shortest_path(distance_graph, last_location)
        truck.distance += distance_graph.hub_vertex.distance
        hub.total_distance += distance_graph.hub_vertex.distance
        print('truck.distance: ', truck.distance)
        truck.finish_time = (truck.distance / 18)
        print('truck.finish_time: ', truck.finish_time)

    hub.finish_time = max(truck_1.finish_time, truck_2.finish_time, truck_3.finish_time)

    for truck in trucks:
        print('Truck {0} path:')
        for path in truck.paths:
            print('## Paths taken: ')
            for v in path:
                print(str(v) + ', ', end=' ')
            print()

    print('Total distance of all trucks: {0:.2f}'.format(hub.total_distance))
    print('All packages delivered at: {0}'.format(get_formatted_time(hub.finish_time)))

    # for truck in [truck_1, truck_2, truck_3]:
    #     if len(truck.delivery_queue) > 0:
    #         for package in truck.delivery_queue:
    #             shortest_v = Model.Location('shortest')
    #             if package.delivery_address in distance_graph.adjacency_list:
    #                 for v in distance_graph.adjacency_list[package.delivery_address]:
    #                     if v.distance < shortest_v.distance:
    #                         shortest_v = v
    #             sorted_packages_by_address = hub.get_packages_by_address(package_list)
    #             if shortest_v.label in sorted_packages_by_address:
    #                 for peer_package in sorted_packages_by_address[shortest_v.label]:
    #                     if truck.load_on_truck(peer_package):
    #                         package_list.remove(peer_package)
    #
    # closest_v = distance_graph.hub_vertex
    # visited = [closest_v]
    # # Sort packages by distance
    # # print(len(distance_graph.adjacency_list))
    # for v1 in visited:
    #     # print(v1.label)
    #     for v2 in distance_graph.adjacency_list[v1]:
    #         # print(' ' * 4, v2.label)
    #         closest_distance = float('inf')
    #         if v2 not in visited and v2.distance < closest_distance:
    #             closest_v = v2
    #     print('closest_v: ', closest_v.label)
    #
    #     if closest_v.label is not 'HUB':
    #         packages_by_address = hub.get_packages_by_address(package_list)
    #         if closest_v not in visited:
    #             visited.append(closest_v)
    #         if closest_v.label in packages_by_address:
    #             for package in packages_by_address[closest_v.label]:
    #                 if truck_1.load_on_truck(package):
    #                     package_list.remove(package)
    #                     continue
    #                 if truck_2.load_on_truck(package):
    #                     package_list.remove(package)
    #                     continue
    #                 if truck_3.load_on_truck(package):
    #                     package_list.remove(package)
    #                     continue
    #                 else:
    #                     print("couldn't load package")
    # #
    # print('#' * 118)
    # print('# Package_List:')
    # print('#' * 118)
    # for package in package_list:
    #     print(package)
    # for truck in [truck_1, truck_2, truck_3]:

    #
    # total_distance = 0
    # start_v = distance_graph.hub_vertex
    # list_of_trucks = [truck_1, truck_2, truck_3]
    #
    # for truck in list_of_trucks:
    #     print('#' * 118)
    #     print('# Truck {0}:'.format(truck.truck_id))
    #     print('#' * 118)
    #     # print(truck.delivery_queue)
    #     if truck.truck_id in [1, 2]:
    #         current_time = hub.start_time
    #     else:
    #         if truck_1.finish_time < truck_2.finish_time:
    #             current_time = truck_1.finish_time
    #             truck.driver = truck_1.driver
    #         else:
    #             current_time = truck_2.finish_time
    #             truck.driver = truck_2.driver
    #
    #     truck.start_time = current_time
    #     packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
    #
    #     for package in truck.delivery_queue:
    #         if package is not None:
    #             for v in distance_graph.adjacency_list[start_v]:
    #                 if v.label == package.delivery_address:
    #                     # print(start_v.label)
    #                     # print(v.label)
    #                     truck.distance = truck.distance + v.distance
    #                     total_distance = total_distance + v.distance
    #                     path = ShortestPath.get_shortest_path(
    #                         start_v, v)
    #                     print('Path from {0}, to {1}: {2} , Distance = {3}'.format(start_v, v, path, v.distance))
    #                     for v2 in path[1:]:
    #                         if v2.label in packages_by_address:
    #                             for other_package in packages_by_address[v2.label]:
    #                                 other_package.delivery_time = (v.distance / 18)
    #                                 other_package.arrival_time = (current_time + other_package.delivery_time)
    #                                 other_package.delivery_status = 'delivered'
    #                                 # print(other_package)
    #
    #                     current_time = current_time + package.delivery_time
    #                     print('The following packages took {0} to deliver and arrived at {1}: \n'.format(
    #                         get_formatted_time(package.delivery_time), get_formatted_time(current_time)))
    #                     print(package)
    #                     print('')
    #                     start_v = v
    #     truck.finish_time = current_time
    #     print(truck)
    #
    # for truck in [truck_1, truck_2, truck_3]:
    #     if truck.finish_time > hub.finish_time:
    #         hub.finish_time = truck.finish_time
    # print('Total distance of all trucks: {0:.2f}'.format(total_distance))
    # print('All packages delivered at: {0}'.format(get_formatted_time(hub.finish_time)))

    # for package in sorted_packages:
    #     print(package)
    # print('Status check results: \n')
    # for time in ['9:00:00', '10:00:00', '13:00:00']:
    #     print(time + ': ')
    #         for package in truck.delivery_queue:
    #             if package is not None:
    #                 print(package)

    # start_v = distance_graph.hub_vertex
    # smallest_v = Model.Location('smallest')
    # smallest_v.distance = float('inf')
    # visited = []
    # while len(package_list) > 0:
    #     ShortestPath.dijkstra_shortest_path(distance_graph, start_v)
    #     packages_by_address = hub.get_packages_by_address(package_list)
    #     for v in distance_graph.adjacency_list[start_v]:
    #         if v.distance < smallest_v.distance and v not in visited:
    #             smallest_v = v
    #     for packages in packages_by_address[smallest_v.label]:
    #         Model.Truck.deliver(package)
    #         package_list.remove(package)
    #     start_v = smallest_v
    #
    # for v in distance_graph.adjacency_list:
    #     vertices = distance_graph.adjacency_list[v]
    #     for i in range(1, len(vertices)):
    #         j = i
    #
    #         while j > 0 and vertices[j].distance < vertices[j - 1].distance:
    #             temp = vertices[j]
    #             vertices[j] = vertices[j - 1]
    #             vertices[j - 1] = temp
    #             j -= 1
    #
    # current_time = hub.start_time
    # total_distance = 0
    # for truck in [truck_1, truck_2, truck_3]:
    #     packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
    #     start_v = distance_graph.hub_vertex
    #     start_v.index = 0
    #     last_v = Model.Location('last_v')
    #     while len(truck.delivery_queue) > 0:
    #         end_v = distance_graph.adjacency_list[start_v][start_v.index]
    #         if end_v == last_v and end_v.label not in packages_by_address:
    #             start_v.index += 1
    #             continue
    #         else:
    #             path = ShortestPath.get_shortest_path(start_v, end_v)
    #             delivery_time = (end_v.distance / 18)
    #             current_time = (current_time + delivery_time)
    #             truck.distance = truck.distance + end_v.distance
    #             total_distance = total_distance + end_v.distance
    #             print('The following packages took {0} to deliver and arrived at {1}: \n'.format(
    #                 get_formatted_time(delivery_time), get_formatted_time(current_time)))
    #             for v in path[1:]:
    #                 if v.label is not 'hub' and v.label in packages_by_address:
    #                     for package in packages_by_address[v.label]:
    #                         package.delivery_status = "delivered"
    #                         package.delivery_time = delivery_time
    #                         package.arrival_time = current_time
    #                         print(package)
    #                         # Deliver package
    #                         # remove package from list
    #                         if package in truck.delivery_queue:
    #                             truck.delivery_queue.remove(package)
    #
    #         start_v.index += 1
    #         start_v = end_v
    #         last_v = end_v
    #     truck.finish_time = current_time
    #
    # for truck in [truck_1, truck_2, truck_3]:
    #     if truck.finish_time > hub.finish_time:
    #         hub.finish_time = truck.finish_time
    # print('Total distance of all trucks: {0:.2f}'.format(total_distance))
    # print('All packages delivered at: {0}'.format(get_formatted_time(hub.finish_time)))


# BubbleSort(numbers, numbersSize) {
# for (i = 0; i < numbersSize - 1; i++) {
# for (j = 0; j < numbersSize - i - 1; j++) {
# if (numbers[j] > numbers[j+1]) {
# temp = numbers[j]
# numbers[j] = numbers[j + 1]
# numbers[j + 1] = temp
# }
# }
# }
# }


# sort_adjacency_lists(distance_graph.hub_vertex, distance_graph)
#
#
#     for package in package_list:
#         if package.delivery_address == v.label:
#             package.deliver()


# TODO: The wrong delivery address for package #9, Third District Juvenile Court, will be corrected at 10:20 a.m. The correct address is 410 S State St., Salt Lake City, UT 84111.


if __name__ == "__main__":
    main()
