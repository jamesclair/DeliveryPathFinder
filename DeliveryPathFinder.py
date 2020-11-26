# James Clair, 000847594

import copy
import datetime
import Model
import Modules

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
        return max(min(trucks[0].finish_time, trucks[1].finish_time), get_hours_float('10:20:00'))
    elif truck.truck_id == 2:
        return get_hours_float('09:05:00')
    else:
        return hub.start_time

def load_special_packages(package_list, trucks):
    original_list = package_list.copy()
    for package in original_list:
        if package.special_note != "":
            note_parts = package.special_note.split(' ')
            print(note_parts[0])
            if note_parts[0] == "Delayed" or note_parts[0] == "Wrong":
                package.delayed = True
                trucks[1].load(package_list, package)
            elif note_parts[-2] == 'truck':
                if note_parts[-1] == '1':
                    trucks[0].load(package_list, package)
                elif note_parts[-1] == '2':
                    trucks[1].load(package_list, package)
                elif note_parts[-1] == '3':
                    trucks[2].load(package_list, package)
            else:
                package.peer_packages.append(note_parts[-2][:-1])
                package.peer_packages.append(note_parts[-1])
                trucks[0].load(package_list, package)
                for p2 in package_list:
                    if p2.package_id in package.peer_packages and p2.delivery_status != 'loaded':
                        trucks[0].load(package_list, p2)
        else:
            if package.delivery_deadline != 'EOD' and package.delivery_status != 'loaded':
                trucks[0].load(package_list, package)

def main():
    package_list = Modules.LoadData.load_packages()
    distance_graph = Modules.LoadData.load_distances()

    hub = Model.Hub()
    trucks = [Model.Truck(1, hub.drivers[0]), Model.Truck(2, hub.drivers[1]), Model.Truck(3)]
    load_special_packages(package_list, trucks)
    
    # load remainder of packages while calculating distance/time
    for truck in trucks:
        starting_location = distance_graph.hub_vertex
        truck.start_time = set_truck_start_time(truck, trucks, hub)
        while len(truck.delivery_queue) > 0:
            # find out the next closest location
            Modules.ShortestPath.dijkstra_shortest_path(distance_graph, starting_location)
            current_location = truck.find_closest_location()
            # what is the path I took to get there?
            path = Modules.ShortestPath.get_shortest_path(starting_location, current_location)
            print(path)
            truck.load_packages_in_path(path, hub)
            # what is that distance?
            truck.distance = truck.distance + current_location.distance

            
            truck.delivery_queue.clear()

            # reset the starting location to current location
            starting_location = current_location
 



if __name__ == "__main__":
    main()
