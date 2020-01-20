# James Clair, 000847594

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


# def check_status(current_time, package_list, hub):
#     packages_by_status = hub.get_packages_by_status(package_list)
#     if ((get_hours_float('8:35:00') <= current_time <= get_hours_float('9:25:00') and hub.count == 0) or (
#             get_hours_float('9:35:00') <= current_time <= get_hours_float('10:25:00') and hub.count == 1) or (
#             get_hours_float('12:03:00') <= current_time <= get_hours_float('13:12:00') and hub.count == 2)):
#         print('*** {0} Status Check ***'.format(get_formatted_time(current_time)))
#         hub.count = hub.count + 1


def main():
    package_list = LoadData.load_packages()
    distance_graph = LoadData.load_distances()

    # print(len(package_list))

    ShortestPath.dijkstra_shortest_path(distance_graph, distance_graph.hub_vertex)

    hub = Model.Hub()
    truck_1 = Model.Truck(1, hub.drivers[0])
    truck_2 = Model.Truck(2, hub.drivers[1])
    truck_3 = Model.Truck(3)  # Driver assigned once first truck returns.
    sorted_packages = []
    visited = []
    packages_by_address = hub.get_packages_by_address(package_list)
    closest_v = None
    # visited.append(closest_v)

    # Sort packages by distance
    # print(len(distance_graph.adjacency_list))
    for v1 in distance_graph.adjacency_list:
        # print(v1.label)
        for v2 in distance_graph.adjacency_list[v1]:
            # print(' ' * 4, v2.label)
            closest_distance = float('inf')
            if v2 not in visited and v2.distance < closest_distance:
                closest_v = v2
        if closest_v is not None:
            visited.append(closest_v)

        if closest_v.label is not 'HUB':
            for package in packages_by_address[closest_v.label]:
                sorted_packages.append(package)

    # Load packages with special notes
    # print(len(sorted_packages))
    for package in sorted_packages:
        # print(package.package_id)

        # Sort packages with special notes
        if package.special_note != "":
            package.delivery_status = 'loaded'
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

                for p2 in sorted_packages:
                    if p2.package_id in package.peer_packages and p2.delivery_status != 'loaded':
                        truck_1.load_on_truck(p2)
                    # if not package_list[p - 1].delivery_status == 'loaded':
                    #     truck_1.load_on_truck(sorted_packages[p - 1])

    print(sorted_packages)
    # Load the rest of packages
    for package in sorted_packages:
        # print(package)
        if package.delivery_status != 'loaded':
            print('not_loaded:', package.package_id, ": ", package.delivery_status)
            if truck_1.load_on_truck(package):
                continue
            elif truck_2.load_on_truck(package):
                continue
            elif truck_3.load_on_truck(package):
                continue
            else:
                print("All trucks are full your hub is overloaded.  Better get that checked out.")
        elif package.delivery_status == 'loaded':
            print('loaded:', package.package_id, ": ", package.delivery_status)
    print('All trucks are loaded')
    # print(truck_1.delivery_queue)
    # print(truck_2.delivery_queue)
    # print(truck_3.delivery_queue)
    # Deliver packages
    total_distance = 0
    start_v = distance_graph.hub_vertex

    list_of_trucks = [truck_1, truck_2, truck_3]
    for truck in list_of_trucks:
        print('#' * 118)
        print('# Truck {0}:'.format(truck.truck_id))
        print('#' * 118)
        # print(truck.delivery_queue)
        if truck.truck_id in [1, 2]:
            current_time = hub.start_time
        else:
            if truck_1.finish_time < truck_2.finish_time:
                current_time = truck_1.finish_time
                truck.driver = truck_1.driver
            else:
                current_time = truck_2.finish_time
                truck.driver = truck_2.driver

        truck.start_time = current_time
        packages_by_address = hub.get_packages_by_address(truck.delivery_queue)

        for package in truck.delivery_queue:
            if package is None:
                continue
            else:

                for v in distance_graph.adjacency_list[start_v]:
                    if v.label == package.delivery_address:
                        truck.distance = truck.distance + v.distance
                        total_distance = total_distance + v.distance
                        print('Path from {0}, to {1}: {2} , Distance = {3}'.format(start_v, v,
                                                                                   ShortestPath.get_shortest_path(
                                                                                       start_v, v), v.distance))
                        for other_package in packages_by_address[v.label]:
                            other_package.delivery_time = (v.distance / 8)
                            other_package.arrival_time = (current_time + other_package.delivery_time)
                            other_package.delivery_status = 'delivered'
                            # print(other_package)

                        current_time = current_time + package.delivery_time
                        print('The following packages took {0} to deliver and arrived at {1}: \n'.format(
                            get_formatted_time(package.delivery_time), get_formatted_time(current_time)))
                        print(package)
                        print('')
        truck.finish_time = current_time
        print(truck)

    for truck in [truck_1, truck_2, truck_3]:
        if truck.finish_time > hub.finish_time:
            hub.finish_time = truck.finish_time
    print('Total distance of all trucks: {0:.2f}'.format(total_distance))
    print('All packages delivered at: {0}'.format(get_formatted_time(hub.finish_time)))

    # for package in sorted_packages:
    #     print(package)
    # print('Status check results: \n')
    # for time in ['9:00:00', '10:00:00', '13:00:00']:
    #     print(time + ': ')
    #         for package in truck.delivery_queue:
    #             if package is not None:
    #                 print(package)


# TODO: The wrong delivery address for package #9, Third District Juvenile Court, will be corrected at 10:20 a.m. The correct address is 410 S State St., Salt Lake City, UT 84111.


if __name__ == "__main__":
    main()
