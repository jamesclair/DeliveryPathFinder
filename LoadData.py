import Model
import csv

hub = Model.Hub()

with open('Packages.csv', mode='r') as packages:
    package_list = hub.package_list
    packages_by_address = Model.PackagePropertyTable(27)
    packages_by_deadline = Model.PackagePropertyTable(40)
    packages_by_city = Model.PackagePropertyTable(40)
    packages_by_zip = Model.PackagePropertyTable(40)
    packages_by_weight = Model.PackagePropertyTable(40)
    packages_by_status = Model.PackagePropertyTable(3)  # hub, in route, delivered
    package_reader = csv.reader(packages, delimiter=',')
    count = 0
    for row in package_reader:
        if count > 0:
            package_id = int(row[0])
            package = Model.Package(package_id=row[0], package_weight=row[6], special_note=row[7],
                                    delivery_address=row[1], delivery_city=row[2], delivery_zip=row[4],
                                    delivery_deadline=row[5], delivery_state=row[3])
            package_list[package_id - 1] = package
        count += 1

with open('Distances.csv', mode='r') as distances:
    distance_graph = Model.DistanceGraph()
    distance_reader = csv.reader(distances, delimiter=',')
    count = 0
    locations = []

    for row in distance_reader:
        if count > 0:
            address = str(row[1])[1:-8]
            location = Model.Location(address)

            if location.label == "":
                location.label = "HUB"
                distance_graph.hub_vertex = location
            distance_graph.add_vertex(location)

            for path in range(2, len(row)):
                if row[path] == '0.0':
                    break
                else:
                    # print("v.label: ", location.label)
                    # print("v.distance: ", location.distance)
                    # print("v.predecessor: ", location.predecessor)
                    # v = list(distance_graph.adjacency_list.keys())[path - 2]
                    # print("secondV_label: ", v.label)
                    # print("secondV_distance: ", v.distance)
                    # print("secondV_predecessor: ", v.predecessor)
                    # print("weight: ", str(float(row[path])))
                    distance_graph.add_undirected_edge(location
                                                       , list(distance_graph.adjacency_list.keys())[path - 2]
                                                       , float(row[path]))

        count += 1
    # for v in distance_graph.adjacency_list:
    #     print("v.label: ", v.label)
    #     print("v.distance: ", v.distance)
    #     print("v.predecessor: ", v.predecessor)

def load_packages():
    return package_list


def load_distances():
    return distance_graph
