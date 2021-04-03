from PackagePropertyTable import PackagePropertyTable

class Hub:
    def __init__(self, capacity=40):
        self.package_list = [None] * capacity
        self.start_time = 8
        self.drivers = ['Bill', 'Ted']
        self.finish_time = 0
        self.count = 0
        self.total_distance = 0
        self.packages_delivered = 0
        self.wrong_address = []

    def get_packages_by_weight(self, packages):
        packages_by_weight = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_weight.create(package.delivery_weight, package)
        return packages_by_weight

    def get_packages_by_zip(self, packages):
        packages_by_zip = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_zip.create(package.delivery_zip, package)
        return packages_by_zip

    def get_packages_by_city(self, packages):
        packages_by_city = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_city.create(package.delivery_city, package)
        return packages_by_city

    def get_packages_by_id(self, packages):
        packages_by_id = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_id.create(package.package_id, package)
        return packages_by_id

    def get_packages_by_status(self, packages):
        packages_by_status = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_status.create(package.delivery_status, package)
        return packages_by_status

    def get_packages_by_address(self, packages):
        packages_by_address = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_address.create(package.delivery_address, package)
        return packages_by_address

    def get_packages_by_deadline(self, packages):
        packages_by_deadline = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_deadline.create(package.delivery_deadline, package)
        return packages_by_deadline

    def get_packages_by_arrival(self, packages):
        packages_by_arrival = PackagePropertyTable(40)
        for package in packages:
            if package is not None:
                packages_by_arrival.create(package.arrival_time, package)
        return packages_by_arrival
