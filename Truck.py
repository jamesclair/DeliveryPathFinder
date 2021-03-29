from PackagePropertyTable import PackagePropertyTable

class Truck:

    def __init__(self, truck_id, driver=""):
        self.MAX_LOAD = 16
        self.AVG_MPH = 18
        self.driver = driver
        self.delivery_queue = []
        self.priority_delivery_queue = []
        self.truck_id = truck_id
        self.packages_delivered = 0
        self.package_count = 0
        self.distance = 0
        self.time = 0
        self.path = []
        self.current_location = None
        self.start_time = 0

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
            package.delivery_status = 'loaded'
            package.truck_id = self.truck_id
            if package.priority:
                self.priority_delivery_queue.append(package)
                print('    result:', package.package_id, 'PRIORITY - loaded on truck', self.truck_id)
            elif package.is_special == True:
                self.delivery_queue.append(package)
                print('    result:', package.package_id, 'SPECIAL - loaded on truck', self.truck_id)
            else:
                print('    result:', package.package_id, 'loaded on truck', self.truck_id)
                self.delivery_queue.append(package)
            self.package_count += 1
            return True
        else:
            print('Package: ', package.package_id, 'unable to load package. Truck: ', self.truck_id, 'is full.')
            return False

    def find_closest_location(self):
        closest_distance = float('inf')
        smallest = None
        for i in range(0, len(self.delivery_queue)):
            # print('location:', self.delivery_queue[i].location.label)
            # print('distance:', self.delivery_queue[i].location.distance)
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

    def load_packages_in_path(self, package_list, path):
        for location in path:
            # any package that has not been loaded to be added to current truck
            # could make this a pre-built map, where packages(values) at a specific location(key) are returned instead
            for package in package_list:
                if package.location == location:
                    print("location in package matched: ", location)
                    if self.load_on_truck(package):
                        package_list.remove(package)

    # def load(self, package_list, package):
    #     if self.load_on_truck(package):
    #         package_list.remove(package)
