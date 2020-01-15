class Package:

    def __init__(self, package_id, package_weight, special_note, delivery_address, delivery_city, delivery_zip,
                 delivery_deadline, delivery_state):
        self.package_id = package_id
        self.package_weight = package_weight
        self.special_note = special_note
        self.delivery_address = delivery_address
        self.city = delivery_city
        self.delivery_city = self.city
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.delivery_state = delivery_state
        self.delivery_time = 0
        self.delivery_status = 'hub'
        self.truck_id = 0
        self.is_wrong_addr = False
        self.peer_packages = []
        self.miles = 0

    def __str__(self):
        return ('package_id: ' + self.package_id.__str__()
                + '\npackage_weight: ' + self.package_weight.__str__()
                + '\nspecial_note: ' + self.special_note
                + '\ndelivery_address: ' + self.delivery_address
                + '\ndelivery_city: ' + self.delivery_city
                + '\ndelivery_zip: ' + self.delivery_zip
                + '\ndelivery_deadline: ' + self.delivery_deadline.__str__()
                + '\n\n'
                )


class Hub:
    def __init__(self, capacity=40):
        self.package_list = [None] * capacity
        self.start_time = 8
        self.drivers = ['Bill', 'Ted']

    def get_packages_by_status(self, packages):
        packages_by_status = {}
        for package in packages:
            if package is not None:
                packages_by_status[package.delivery_status].append(package)
        return packages_by_status

    def get_packages_by_address(self, packages):
        packages_by_address = {}
        for package in packages:
            if package is not None:
                if package.delivery_address in packages_by_address:
                    packages_by_address[package.delivery_address].append(package)
                else:
                    packages_by_address[package.delivery_address] = []
                    packages_by_address[package.delivery_address].append(package)
        return packages_by_address

    def get_packages_by_deadline(self, packages):
        packages_by_deadline = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_deadline.create(package.delivery_deadline, package)
        return packages_by_deadline

    def get_packages_by_city(self, packages):
        packages_by_city = {}
        for package in packages:
            if package is not None:
                packages_by_city[package.delivery_city].append(package)
        return packages_by_city

    def get_packages_by_zip(self, packages):
        packages_by_zip = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_zip.create(package.delivery_zip, package)
        return packages_by_zip

    def get_packages_by_weight(self, packages):
        packages_by_weight = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_weight.create(package.delivery_weight, package)
        return packages_by_weight

    # def get_packages_by_distance(self, packages):
    #     for package in packages:
    #         for v in


class Truck:

    def __init__(self, truck_id, driver=""):
        self.MAX_LOAD = 16
        self.AVG_MPH = 18
        self.DELIVERY_TIME = 0
        self.driver = driver
        self.delivery_queue = [None] * self.MAX_LOAD
        self.truck_id = truck_id
        self.package_count = 0
        self.distance = 0
        self.finish_time = 0

    # TODO: Add 1 driver to two trucks and 1 driver to the other truck
    def __str__(self):
        return ('MAX_LOAD: ' + self.MAX_LOAD.__str__()
                + '\nAVG_MPH: ' + self.AVG_MPH.__str__()
                + '\ndriver: ' + self.driver.__str__()
                + '\nDELIVERY_TIME_SECONDS: ' + self.DELIVERY_TIME.__str__()
                + '\n\n'
                )

    def load_on_truck(self, package):
        if self.package_count < 16:
            self.delivery_queue.append(package)
            package.delivery_status = 'loaded'
            package.truck_id = self.truck_id
            self.package_count += 1
            print('Package', package.package_id, 'loaded on truck', self.truck_id)
            return True
        else:
            print('Package: ', package.package_id, 'unable to load package. Truck: ', self.truck_id, 'is full.')
            return False


class PackagePropertyTable:

    def __init__(self, size):
        self.table = []
        self.keys = []
        for i in range(size):
            self.table.append([])

    def create(self, key, value):
        key = int(key)
        bucket = hash(key) % len(self.table)
        self.table[bucket].append(value)
        self.keys.append(key)

    def read(self, key):
        key = int(key)
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        return bucket_list[0]

    def delete(self, key):
        key = int(key)
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if bucket in bucket_list:
            bucket_list.remove(bucket)


class Location:
    def __init__(self, label):
        self.label = label
        self.distance = float('inf')
        self.predecessor = None

    def __str__(self):
        return str(self.label)


class DistanceGraph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}
        self.hub_vertex = Location('hub')

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)
