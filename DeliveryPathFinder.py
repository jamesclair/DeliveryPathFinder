# James Clair, 000847594

import copy
import LoadData
import Time
import ShortestPath

from Hub import Hub
from Truck import Truck
from Package import Package
from Location import Location


def check_status(current_time, hub, packages):
    print()
    packages_by_status = hub.get_packages_by_status(packages)
    if ((Time.get_hours_float('8:35:00') <= current_time <= Time.get_hours_float('9:25:00') and hub.count == 0) or (
            Time.get_hours_float('9:35:00') <= current_time <= Time.get_hours_float('10:25:00') and hub.count == 1) or (
            Time.get_hours_float('12:03:00') <= current_time <= Time.get_hours_float('13:12:00') and hub.count == 2)):
        print('*** {0} Status Check ***'.format(Time.get_formatted_time(current_time)))
        print()
        print('loaded: ', end="")
        if packages_by_status.read('loaded') is not None:
            for package in packages_by_status.read('loaded'):
                print(package.package_id, end=", ")
        print()
        print('delivered: ', end="")
        for package in packages_by_status.read('delivered'):
            print(package.package_id, end=", ")
        print('\n*** End of Status check ***\n')
        hub.count = hub.count + 1


# Total runtime complexity = O(N) + O(N^3) + O(N^3) + O(N^3) = O(N^3)
def main():
    packages = LoadData.load_packages()
    distance_graph = LoadData.load_distances()

    hub = Hub()
    print("<------------Processing and loading special packages on trucks---------------->")
    trucks = [Truck(1, hub.drivers[0]), Truck(2, hub.drivers[1]), Truck(3)]
    packages_by_id = hub.get_packages_by_id(packages)
    unloaded_packages = []

    # Run-time complexity: O(N) * O(1) = O(N)
    for package in packages:
        print("Package: ", package.package_id, "with a delivery deadline of: ", package.delivery_deadline, "and special note: ", package.special_note)
        if package.delivery_deadline != 'EOD':
            package.priority=True
        if package.special_note != "":
            package.is_special = True
            note_parts = package.special_note.split(' ')
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
                # Run-time complexity: O(1)
                for p2 in package.peer_packages:
                    peer_package = packages_by_id.read(p2)
                    if package.priority == True:
                        peer_package[0].priority=True
                    if peer_package[0].delivery_status != 'loaded':
                        trucks[0].load_on_truck(peer_package[0])
        elif package.priority and package.delivery_status != 'loaded':
            trucks[0].load_on_truck(package)
        elif package.delivery_status == 'loaded':
           print("    result: ", package.package_id, "Has already been loaded.  Nothing to do.") 
        else:
            print("    result: ", package.package_id, "Not special, will be loaded after special packages are processed/loaded.")
            unloaded_packages.append(package)
    print("<------------Special packages loaded---------------->\n")
    
    # load all remainder of packages on trucks optimized for distance
    print("<------------Load remaining packages---------------->")
    packages_by_address = hub.get_packages_by_address(unloaded_packages)
    loaded_packages = []
    # O(N) * (O(1) + O(N^2) + O(N) + O(1)) = O(N^3)
    while len(unloaded_packages) > 0:
        for truck in trucks:
            # if it's the trucks first iteration
            if truck.current_location == None:
                # set the trucks starting location
                truck.current_location = distance_graph.hub_vertex
            for v in distance_graph.adjacency_list:
                v.distance = float('inf')
                v.predecessor = None
            ShortestPath.dijkstra_shortest_path(distance_graph, truck.current_location)
            # find the location with the next closest distance
            closest_distance = float('inf')
            smallest = None
            # Run-time complexity: O(N)
            for i in range(0, len(unloaded_packages)):
                if unloaded_packages[i].location.distance < closest_distance:
                    smallest = i
                    closest_distance = unloaded_packages[i].location.distance

            packages_at_stop = packages_by_address.read(unloaded_packages[smallest].location.label)
            if len(packages_at_stop) < (16 - truck.package_count):
                starting_location = truck.current_location
                truck.current_location = unloaded_packages[smallest].location
                
                # load all packages at this address
                # run-time complexity O(1)
                for package in packages_at_stop:
                    print("Package: ", package.package_id)
                    if package.location.label == truck.current_location.label and truck.load_on_truck(package):
                        loaded_packages.append(package)
                        unloaded_packages.remove(package)
            else:
                continue
    print("<------------All packages loaded---------------->\n")

    # deliver all packages calculating distance
    print("<------------Deliver packages---------------->\n")
    trucks[0].start_time = hub.start_time
    trucks[1].start_time = Time.get_hours_float('09:05:00')
    trucks[2].start_time = max(min(trucks[0].time, trucks[1].time), Time.get_hours_float('10:20:00'))
    count = 0
    package_ids = []
    for truck in trucks:
        print("<------------Deliver Truck: ", truck.truck_id, " PRIORITY packages---------------->")
        
        packages_by_address = hub.get_packages_by_address(truck.priority_delivery_queue)
        truck.current_location = distance_graph.hub_vertex
        # O(N) * O(1) * O(N^2) * O(N) * O(1) = O(N^3)
        while len(truck.priority_delivery_queue) > 0:
            # Run-time complexity: O(1)
            for v in distance_graph.adjacency_list:
                v.distance = float('inf')
                v.predecessor = None
            # Using a simple list so O(N^2) runtime complexity
            ShortestPath.dijkstra_shortest_path(distance_graph, truck.current_location)
            # find the location with the next closest distance
            closest_distance = float('inf')
            smallest = None
            # Run-time complexity: O(N)
            for i in range(0, len(truck.priority_delivery_queue)):
                if truck.priority_delivery_queue[i].location.distance < closest_distance:
                    smallest = i
                    closest_distance = truck.priority_delivery_queue[i].location.distance
            starting_location = truck.current_location
            truck.current_location = truck.priority_delivery_queue[smallest].location
            truck.distance += closest_distance
            truck.time = truck.start_time + (truck.distance / 18)
            check_status(truck.time, hub, packages)
            truck.path.append(ShortestPath.get_shortest_path(starting_location, truck.current_location))
            # at best run-time complexity O(1) at worst run-time complexity of O(N)
            for package in packages_by_address.read(truck.current_location.label):
                if package.location.label == truck.current_location.label:
                    truck.priority_delivery_queue.remove(package)
                    package.deliver_package(truck.start_time + (truck.distance / 18))
                    package_ids.append(package.package_id)
                    count += 1
                    print(package, "\n")

        truck.time = truck.start_time + (truck.distance / 18)
        print("<------------Truck: ", truck.truck_id, " PRIORITY packages delivered---------------->\n")

    for truck in trucks:
        print("<------------Deliver Truck: ", truck.truck_id, " packages---------------->")
        packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
        truck.current_location = distance_graph.hub_vertex
        # O(N) * (O(1) + O(N^2) + O(N) + O(1)) = O(N^3))
        while len(truck.delivery_queue) > 0:
            # Run-time complexity: O(1)
            for v in distance_graph.adjacency_list:
                v.distance = float('inf')
                v.predecessor = None
            # Using a simple list so O(N^2) runtime complexity
            ShortestPath.dijkstra_shortest_path(distance_graph, truck.current_location)
            # find the location with the next closest distance
            closest_distance = float('inf')
            smallest = None
            # Run-time complexity: O(N)
            for i in range(0, len(truck.delivery_queue)):
                if truck.delivery_queue[i].location.distance < closest_distance:
                    smallest = i
                    closest_distance = truck.delivery_queue[i].location.distance
            starting_location = truck.current_location
            truck.current_location = truck.delivery_queue[smallest].location
            truck.distance += closest_distance
            truck.time = truck.start_time + (truck.distance / 18)
            check_status(truck.time, hub, packages)
            truck.path.append(ShortestPath.get_shortest_path(starting_location, truck.current_location))
            if truck.truck_id == 2 and truck.time >= 10.33:
                package_nine = packages_by_id.read('9')[0]
                package_nine.delivery_address = '410 S State St'
                package_nine.delivery_city = 'Salt Lake City'
                package_nine.delivery_state = 'UT' 
                package_nine.zip = '84111'
                for l in distance_graph.adjacency_list:
                    if l.label == '410 S State St':
                        package_nine.location = l
                packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
            
            # run-time complexity O(1)
            for package in packages_by_address.read(truck.current_location.label):
                if package.location.label == truck.current_location.label:
                    truck.delivery_queue.remove(package)
                    package.deliver_package(truck.time)
                    package_ids.append(package.package_id)
                    count += 1
                    print(package, "\n")

        truck.time = truck.start_time + (truck.distance / 18)
        print("<------------Truck: ", truck.truck_id, " packages delivered---------------->\n")

    # report time finished and distance of each truck and total distance of all trucks
    total_distance = trucks[0].distance + trucks[1].distance + trucks[2].distance
    
    # TODO: An interface that allows the user to enter a time to check the status of a package or all packages at a given time is not readily evident
    print("<----------------------------STATUS CHECK------------------------------>")
    print()
    user_time_fmt = input("To check the delivery status, please enter a time in HH:MM:SS format: ")
    user_time = Time.get_hours_float(user_time_fmt)
    delivered_packages = []
    undelivered_packages = []
    for package in packages:
        if package.arrival_time < user_time:
            delivered_packages.append(package)
        else:
            undelivered_packages.append(package)

    print("<-----------Delivered packages, at", user_time_fmt, "---------->")
    for package in delivered_packages:
        print(
            "package_id: ", package.package_id,
            ", truck: ", package.truck_id,
            ", status: delivered",
            ", address: ", package.delivery_address,
            ", deadline: ", package.delivery_deadline,
            ", city: ", package.delivery_city,
            ", zip: ", package.delivery_zip,
            ", weight: ", package.package_weight
            )
    print("\n")
    print("<-----------Undelivered packages, at", user_time_fmt, "---------->")
    for package in undelivered_packages:
        print(
            "package_id: ", package.package_id,
            ", truck: ", package.truck_id,
            ", status: undelivered",
            ", address: ", package.delivery_address,
            ", deadline: ", package.delivery_deadline,
            ", city: ", package.delivery_city,
            ", zip: ", package.delivery_zip,
            ", weight: ", package.package_weight
            )
    print("\n")
            
    final_report = input("Show FINAL REPORT? (y/n): ")
    if final_report == "y":
        print("<----------------------------FINAL REPORT------------------------------>\n")
        print("Total # of packages delivered: ", count)
        print("Total distance traveled: ", total_distance, "\n")
    
        print("<------------Truck 1---------------->")
        print("Total distance: ", trucks[0].distance)
        print("Time Finished: ", Time.get_formatted_time(trucks[0].time), "\n")
        print(trucks[0].path)

        print("<------------Truck 2---------------->")
        print("Total distance: ", trucks[1].distance)
        print("Time Finished: ", Time.get_formatted_time(trucks[1].time), "\n")
        print(trucks[1].path)

        print("<------------Truck 3---------------->")
        print("Total distance: ", trucks[2].distance)
        print("Time Finished: ", Time.get_formatted_time(trucks[2].time), "\n")
        print(trucks[2].path)
    else:
        print("Skipping Final Report")

if __name__ == "__main__":
    main()
