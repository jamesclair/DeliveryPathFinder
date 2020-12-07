# James Clair, 000847594

import copy
import datetime
import LoadData
from Hub import Hub
from Truck import Truck
import ShortestPath
from Package import Package

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

def check_status(current_time, hub):
    print()
    packages_by_status = hub.get_packages_by_status()
    if ((get_hours_float('8:35:00') <= current_time <= get_hours_float('9:25:00') and hub.count == 0) or (
            get_hours_float('9:35:00') <= current_time <= get_hours_float('10:25:00') and hub.count == 1) or (
            get_hours_float('12:03:00') <= current_time <= get_hours_float('13:12:00') and hub.count == 2)):
        print('*** {0} Status Check ***'.format(get_formatted_time(current_time)))
        print()
        print('loaded: ', end="")
        if packages_by_status.read('loaded') is not None:
            for package in packages_by_status.read('loaded'):
                print(package.package_id, end=", ")
        print()
        print('delivered: ', end="")
        for package in packages_by_status.read('delivered'):
            print(package.package_id, end=", ")
        hub.count = hub.count + 1
    print()
    print()

def set_truck_start_time(truck, trucks, hub):
    if truck.truck_id == 3:
        truck.start_time = max(min(trucks[0].finish_time, trucks[1].finish_time), get_hours_float('10:20:00'))
    elif truck.truck_id == 2:
        truck.start_time = get_hours_float('09:05:00')
    else:
        truck.start_time = hub.start_time

def load_special_packages(package_list, trucks):
    for package in package_list:
        if package.special_note != "":
            note_parts = package.special_note.split(' ')
            print(note_parts[0])
            if note_parts[0] == "Delayed" or note_parts[0] == "Wrong":
                package.delayed = True
                trucks[1].load_on_truck(package)
            elif note_parts[-2] == 'truck':
                if note_parts[-1] == '1':
                    trucks[0].load_on_truck(package)
                elif note_parts[-1] == '2':
                    trucks[1].load_on_truck(package)
                elif note_parts[-1] == '3':
                    trucks[2].load_on_truck(package)
            else:
                package.peer_packages.append(note_parts[-2][:-1])
                package.peer_packages.append(note_parts[-1])
                trucks[0].load_on_truck(package)
                for p2 in package_list:
                    if p2.package_id in package.peer_packages and p2.delivery_status != 'loaded':
                        trucks[0].load_on_truck(p2)
        else:
            if package.delivery_deadline != 'EOD' and package.delivery_status != 'loaded':
                trucks[0].load_on_truck(package)

def main():
    package_list = LoadData.load_packages()
    distance_graph = LoadData.load_distances()

    hub = Hub()
    trucks = [Truck(1, hub.drivers[0]), Truck(2, hub.drivers[1]), Truck(3)]
    load_special_packages(package_list, trucks)
    
    # # load remainder of packages while calculating distance/time
    # for truck in trucks:
    #     starting_location = distance_graph.hub_vertex
    #     set_truck_start_time(truck, trucks, hub)
    #     truck.finish_time = truck.start_time
    #     while len(truck.delivery_queue) > 0:
    #         # find next closest location
    #         ShortestPath.dijkstra_shortest_path(distance_graph, starting_location)
    #         current_location = truck.find_closest_location()
    #         # what is the path I took to get there?
    #         path = ShortestPath.get_shortest_path(starting_location, current_location)
    #         truck.load_packages_in_path(package_list, path)
    #         # update truck distance and time
            
    #         truck.distance = truck.distance + current_location.distance
    #         truck.finish_time = truck.finish_time + (current_location.distance / 18)

    #         packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
    #         for address in path:
    #             print(packages_by_address.read(address))
    #             for package in packages_by_address.read(address):
    #                 package.deliver_package(truck.finish_time)
    #                 truck.delivery_queue.remove(package)
    #         # reset the starting location to current location
    #         starting_location = current_location

# TODO: write a loop for delivering special packages
# NOTE: you will likely need to move the "if it's the trucks first iteration to the new loop"
    while len(package_list) > 0:
        for truck in trucks:
            # if it's the trucks first iteration
            if truck.current_location == None:
                # set the trucks starting location and start time
                truck.current_location = distance_graph.hub_vertex
                if truck.truck_id == 3:
                    truck.start_time = max(min(trucks[0].finish_time, trucks[1].finish_time), get_hours_float('10:20:00'))
                elif truck.truck_id == 2:
                    truck.start_time = get_hours_float('09:05:00')
                else:
                    truck.start_time = hub.start_time

            # find the location with the next closest distance
            ShortestPath.dijkstra_shortest_path(distance_graph, truck.current_location)
            closest_distance = float('inf')
            smallest = None
            for i in range(0, len(package_list)):
                if package_list[i].location.distance < closest_distance:
                    smallest = i
                    closest_distance = package_list[i].location.distance
            truck.current_location = package_list[smallest].location

            # add all packages in path to truck's delivery queue
            # remove all loaded packages from package_list
            # add distance to truck
            # add time taken to truck

# TODO: calculate truck distances and time and report
    for package in package_list:
        if package.distance == None or package.distance > current_location.distance:
            package.distance = current_location.distance
            truck.
        print(package)

if __name__ == "__main__":
    main()
