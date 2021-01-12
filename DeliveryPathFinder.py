# James Clair, 000847594

import copy
import LoadData
import Time
import ShortestPath

from Hub import Hub
from Truck import Truck
from Package import Package

def check_status(current_time, hub):
    print()
    packages_by_status = hub.get_packages_by_status()
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
        hub.count = hub.count + 1
    print()


def main():
    packages = LoadData.load_packages()
    distance_graph = LoadData.load_distances()


    hub = Hub()
    print("<------------Load special packages on trucks---------------->")
    trucks = [Truck(1, hub.drivers[0]), Truck(2, hub.drivers[1]), Truck(3)]
    unloaded_packages = []
    for package in packages:
        print(package)
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
                for p2 in packages:
                    if p2.package_id in package.peer_packages and p2.delivery_status != 'loaded':
                        trucks[0].load_on_truck(p2)
        elif package.delivery_deadline != 'EOD' and package.delivery_status != 'loaded':
            trucks[0].load_on_truck(package)
        else:
            unloaded_packages.append(package)
    print("<------------Special packages loaded---------------->\n")
    
    # load all remainder of packages on trucks optimized for distance
    print("<------------Load remaining packages---------------->")
    packages_by_address = hub.get_packages_by_address(unloaded_packages)
    loaded_packages = []
    while len(unloaded_packages) > len(loaded_packages):
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
            for i in range(0, len(unloaded_packages)):
                if unloaded_packages[i].location.distance < closest_distance:
                    smallest = i
                    closest_distance = unloaded_packages[i].location.distance
            if len(packages_by_address.read(truck.current_location.label)) < (16 - len(truck.delivery_queue)):
                starting_location = truck.current_location
                truck.current_location = unloaded_packages[smallest].location
                
                # load all packages at this address
                for package in packages_by_address.read(truck.current_location.label):
                    if truck.load_on_truck(package):
                        loaded_packages.append(package)
            else:
                continue
    print("<------------All packages loaded---------------->\n")

    # deliver all packages calculating distance
    print("<------------Deliver packages---------------->\n")
    trucks[0].time = hub.start_time
    trucks[1].time = Time.get_hours_float('09:05:00')
    trucks[2].time = max(min(trucks[0].time, trucks[1].time), Time.get_hours_float('10:20:00'))
    count = 0
    package_ids = []
    for truck in trucks:
        print("<------------Deliver Truck: ", truck.truck_id, " packages---------------->")
        if truck.truck_id == 0:
            truck.time = hub.start_time
        elif truck.truck_id == 1:
            truck.time = Time.get_hours_float('09:05:00')
        else:
            truck.time = max(min(trucks[0].time, trucks[1].time), Time.get_hours_float('10:20:00'))
        
        packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
        truck.current_location = distance_graph.hub_vertex
        while len(truck.delivery_queue) > 0:
            for v in distance_graph.adjacency_list:
                v.distance = float('inf')
                v.predecessor = None
            ShortestPath.dijkstra_shortest_path(distance_graph, truck.current_location)
            # find the location with the next closest distance
            closest_distance = float('inf')
            smallest = None
            for i in range(0, len(truck.delivery_queue)):
                if truck.delivery_queue[i].location.distance < closest_distance:
                    smallest = i
                    closest_distance = truck.delivery_queue[i].location.distance
            starting_location = truck.current_location
            truck.current_location = truck.delivery_queue[smallest].location
            truck.distance += closest_distance
            truck.path.append(ShortestPath.get_shortest_path(starting_location, truck.current_location))
            
            for package in packages_by_address.read(truck.current_location.label):
                truck.delivery_queue.remove(package)
                package.deliver_package(truck.time + (truck.distance / 18))
                package_ids.append(package.package_id)
                count += 1
                print(package, "\n")

        truck.time = truck.time + (truck.distance / 18)
        print("<------------Truck: ", truck.truck_id, " packages delivered---------------->\n")

    for package_id in package_ids:
        print(package_id)
    # report time finished and distance of each truck and total distance of all trucks
    total_distance = trucks[0].distance + trucks[1].distance + trucks[2].distance

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

if __name__ == "__main__":
    main()
