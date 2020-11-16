import PackagePropertyTable

class Truck:

    def __init__(self, truck_id, driver=""):
        self.MAX_LOAD = 16
        self.AVG_MPH = 18
        self.driver = driver
        self.delivery_queue = []
        self.truck_id = truck_id
        self.packages_delivered = 0
        self.package_count = 0
        self.distance = 0
        self.finish_time = 0
        self.start_time = 0
        self.paths = []
        self.packages_by_address = PackagePropertyTable(40)
        self.packages_by_zip = PackagePropertyTable(40)
        self.packages_by_city = PackagePropertyTable(40)

    # TODO: Add 1 driver to two trucks and 1 driver to the other truck
    def __str__(self):
        return ('Truck ID: ' + self.truck_id.__str__()
                + '\nStart Time: ' + self.start_time.__str__()
                + '\nDistance: ' + self.distance.__str__()
                + '\nPackage Count: ' + self.package_count.__str__()
                + '\nFinish Time: ' + self.finish_time.__str__()
                + '\nMAX_LOAD: ' + self.MAX_LOAD.__str__()
                + '\nAVG_MPH: ' + self.AVG_MPH.__str__()
                + '\nDriver: ' + self.driver.__str__()
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


    # Todo: add to truck
    def find_closest_location(self):
        closest_distance = float('inf')
        smallest = None
        for i in range(0, len(self.delivery_queue)):
            print('location:', self.delivery_queue[i].location.label)
            print('distance:', self.delivery_queue[i].location.distance)
            if self.delivery_queue[i].location.distance < closest_distance:
                smallest = i
                closest_distance = self.delivery_queue[i].location.distance
        # TODO: Not sure why I should have to check for smallest, but this indicates either there are no packages in the queue
        # OR the packages locations are unset maybe?
        # That would mean an unassigned value is not less than float('inf')...
        if smallest is not None:
            return self.delivery_queue[smallest].location
        else:
            return None

    def load_packages_in_path(self, path, hub):
        for location in path:
            # any package that has not been loaded to be added to current truck
            # could make this a pre-built map, where packages(values) at a specific location(key) are returned instead
            for package in hub.package_list:
                if package.location == location:
                    print("location in package matched: ", location)
                    if self.load_on_truck(package):
                        hub.package_list.remove(package)

    def load(self, hub, package):
        if self.load_on_truck(package):
            hub.package_list.remove(package)

# TODO: fix
def load_special_packages(package_list, trucks):
    original_list = package_list.copy()
    for package in original_list:
        if package.special_note != "":
            note_parts = package.special_note.split(' ')
            print(note_parts[0])
            if note_parts[0] == "Delayed" or note_parts[0] == "Wrong":
                package.delayed = True
                load(package_list, trucks[1], package)
            elif note_parts[-2] == 'truck':
                if note_parts[-1] == '1':
                    load(package_list, trucks[0], package)
                elif note_parts[-1] == '2':
                    load(package_list, trucks[1], package)
                elif note_parts[-1] == '3':
                    load(package_list, trucks[2], package)
            else:
                package.peer_packages.append(note_parts[-2][:-1])
                package.peer_packages.append(note_parts[-1])
                load(package_list, trucks[0], package)
                for p2 in package_list:
                    if p2.package_id in package.peer_packages and p2.delivery_status != 'loaded':
                        load(package_list, trucks[0], p2)
        else:
            if package.delivery_deadline != 'EOD' and package.delivery_status != 'loaded':
                load(package_list, trucks[0], package)


