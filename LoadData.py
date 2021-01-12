import csv
from Hub import Hub
from Package import Package
from DistanceGraph import DistanceGraph
from PackagePropertyTable import PackagePropertyTable
from Location import Location

hub = Hub()

with open('Data/Packages.csv', mode='r') as packages:
    package_list = hub.package_list
    packages_by_address = PackagePropertyTable(27)
    packages_by_deadline = PackagePropertyTable(40)
    packages_by_city = PackagePropertyTable(40)
    packages_by_zip = PackagePropertyTable(40)
    packages_by_weight = PackagePropertyTable(40)
    packages_by_status = PackagePropertyTable(3)  # hub, in route, delivered
    package_reader = csv.reader(packages, delimiter=',')
    count = 0
    for row in package_reader:
        if count > 0:
            package_id = int(row[0])
            package = Package(package_id=row[0], package_weight=row[6], special_note=row[7],
                                    delivery_address=row[1], delivery_city=row[2], delivery_zip=row[4],
                                    delivery_deadline=row[5], delivery_state=row[3])
            package_list[package_id - 1] = package
        count += 1

with open('Data/Distances.csv', mode='r') as distances:
    distance_graph = DistanceGraph()
    distance_reader = csv.reader(distances, delimiter=',')
    count = 0
    locations = []

    for row in distance_reader:
        if count > 0:
            address = str(row[1])[1:-8]
            location = Location(address)

            if location.label == "":
                location.label = 'hub'
                distance_graph.hub_vertex = location
            distance_graph.add_vertex(location)
            for package in package_list:
                if package.delivery_address == location.label:
                    package.location = location

            for path in range(2, len(row)):
                if row[path] == '0.0':
                    break
                else:
                    # print("v.label: ", location.label)
                    v = list(distance_graph.adjacency_list.keys())[path - 2]
                    # print("secondV_label: ", v.label)
                    # print("weight: ", str(float(row[path])))
                    distance_graph.add_undirected_edge(location
                                                       , list(distance_graph.adjacency_list.keys())[path - 2]
                                                       , float(row[path]))

        count += 1
    # for v in distance_graph.adjacency_list:
        # print("v.label: ", v.label)
        # print("v.distance: ", v.distance)
        # print("v.predecessor: ", v.predecessor)


def load_packages():
    return package_list


def load_distances():
    return distance_graph
