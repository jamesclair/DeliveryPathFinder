# DeliveryPathFinder

This will be where I add my algorithm breakdown.


## Past attempts

```python
    # how long did it take to get there?
    # convert time to a time object
    time_to_deliver_package = current_location.distance / 18
    
    print("delivery took: ", get_formatted_time(time_to_deliver_package))
    # TODO: load all packages that match addresses in that path on to the truck
    for location in path:
        if hub.get_packages_by_address.read(location) is not None:
            truck.append(hub.get_packages_by_address.read(location))
            hub.get_packages_by_addres.delete(location)

    hub.get_packages_by_address(package_list)
    if truck.packages_by_address.read(location)

    for package in packages_by_address.read(current_location.label):

    for package in package_list:
        if truck_1_packages_by_address.read(package.delivery_address) is not None:
            if truck_1.load_on_truck(package):
                continue
        if truck_2_packages_by_address.read(package.delivery_address) is not None:
            if truck_2.load_on_truck(package):
                continue
        if truck_3_packages_by_address.read(package.delivery_address) is not None:
            if truck_3.load_on_truck(package):
                continue
        if truck_1_packages_by_zip.read(package.delivery_zip) is not None:
            if truck_1.load_on_truck(package):
                continue
        if truck_2_packages_by_zip.read(package.delivery_zip) is not None:
            if truck_2.load_on_truck(package):
                continue
        if truck_3_packages_by_zip.read(package.delivery_zip) is not None:
            if truck_3.load_on_truck(package):
                continue
        if truck_1_packages_by_city.read(package.delivery_city) is not None:
            if truck_1.load_on_truck(package):
                continue
        if truck_2_packages_by_city.read(package.delivery_city) is not None:
            if truck_2.load_on_truck(package):
                continue
        if truck_3_packages_by_city.read(package.delivery_city) is not None:
            if truck_3.load_on_truck(package):
                continue
        else:
            if truck_1.load_on_truck(package):
                continue
            if truck_2.load_on_truck(package):
                continue
            if truck_3.load_on_truck(package):
                continue
            else:
                print('Unable to load package on truck')

    for truck in trucks:
        print('#' * 118)
        print('# Truck {0}:'.format(truck.truck_id))
        print('# Truck {0} delivery queue length: {1}'.format(truck.truck_id, len(truck.delivery_queue)))
        print('#' * 118)
        for package in truck.delivery_queue:
            print(package.package_id)

    # Deliver packages
    last_location = distance_graph.hub_vertex
    truck_1.start_time = hub.start_time
    truck_2.start_time = get_hours_float('09:05:00')
    for truck in trucks:
        # set the current time
        ShortestPath.dijkstra_shortest_path(distance_graph, last_location)
        if truck.truck_id == 3:
            truck.start_time = min(truck_1.finish_time, truck_2.finish_time)
            truck.start_time = max(truck.start_time, get_hours_float('10:20:00'))
            # hub.wrong_address[0].delivery_address = '410 S State St.'
            # for v in distance_graph.adjacency_list:
            #     if v.label == hub.wrong_address[0].delivery_address:
            #         hub.wrong_address[0].location = v
            # hub.wrong_address[0].delivery_city = 'Salt Lake City'
            # hub.wrong_address[0].delivery_zip = '84111'
            # truck_3.load_on_truck(hub.wrong_address[0])
        print('# Truck {0} start: {1}'.format(truck.truck_id, truck.start_time))
        current_time = truck.start_time

        # Deliver packages with a Deadline
        count = 0
        deadline_packages = []
        for package in truck.delivery_queue:
            if package.delivery_deadline != 'EOD':
                deadline_packages.append(package)

        current_location = find_closest_location(deadline_packages)
        while len(deadline_packages) > 0:
            print('last_total: {0} '.format(hub.total_distance), end='')
            print('+ distance from last: {0} = '.format(current_location.distance), end='')
            hub.total_distance += current_location.distance
            print('new_total: {0}'.format(hub.total_distance))

            print('last_truck_distance: {0} '.format(truck.distance), end='')
            print('+ distance from last: {0} = '.format(current_location.distance), end='')
            truck.distance += current_location.distance
            print('new_truck_distance: {0}'.format(truck.distance))
            current_time = truck.start_time + (truck.distance / 18)
            print('current_time: ', current_time)

            packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
            for package in packages_by_address.read(current_location.label):
                deliver_package(package, current_time)
                if package in deadline_packages:
                    deadline_packages.remove(package)
                    # print(deadline_packages)
                truck.delivery_queue.remove(package)
                print(package)
                count += 1

            # Run status check
            check_status(current_time, original_list, hub)

            last_location = current_location
            # Run dijkstras
            for v in distance_graph.adjacency_list:
                v.distance = float('inf')
                v.predecessor = None
            ShortestPath.dijkstra_shortest_path(distance_graph, current_location)

            # Update next location
            current_location = find_closest_location(deadline_packages)

            # Update the truck's path
            truck.paths.append(ShortestPath.get_shortest_path(last_location, current_location))

        # first location
        current_location = find_closest_location(truck.delivery_queue)

        # Deliveries
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
            current_time = truck.start_time + (truck.distance / 18)
            print('current_time: ', current_time)
            print('current_location.label: ', current_location.label)

            packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
            for package in packages_by_address.read(current_location.label):
                deliver_package(package, current_time)
                truck.delivery_queue.remove(package)
                print(package)
                count += 1

            # Run status check
            check_status(current_time, original_list, hub)

            last_location = copy.deepcopy(current_location)
            # Run dijkstras
            for v in distance_graph.adjacency_list:
                v.distance = float('inf')
                v.predecessor = None
            ShortestPath.dijkstra_shortest_path(distance_graph, current_location)

            # Update next location
            current_location = find_closest_location(truck.delivery_queue)
            # print('last_location:', last_location.label)
            # if current_location is not None:
            #     print('current_location:', current_location.label)
            # print('running shortest path')
            truck.paths.append(ShortestPath.get_shortest_path(last_location, current_location))

        # Return the truck to the hub
        ShortestPath.dijkstra_shortest_path(distance_graph, last_location)
        truck.paths.append(ShortestPath.get_shortest_path(last_location, distance_graph.hub_vertex))
        truck.distance += distance_graph.hub_vertex.distance
        hub.total_distance += distance_graph.hub_vertex.distance
        truck.finish_time = truck.start_time + (truck.distance / 18)
        truck.packages_delivered = count

        # Run status check
        check_status(truck.finish_time, original_list, hub)

        print(truck)

    hub.finish_time = max(truck_1.finish_time, truck_2.finish_time, truck_3.finish_time)
    hub.packages_delivered = truck_1.packages_delivered + truck_2.packages_delivered + truck_3.packages_delivered

    for truck in trucks:
        print('Truck {0} path:'.format(truck.truck_id))
        for path in truck.paths:
            print(path)

    print('Total distance of all trucks: {0:.2f}'.format(hub.total_distance))
    print('All packages delivered at: {0}'.format(get_formatted_time(hub.finish_time)))
    print('Total packages delivered: ', hub.packages_delivered)

```