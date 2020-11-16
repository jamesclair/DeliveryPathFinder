import PackagePropertyTable

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
                packages_by_id.create(package.delivery_id, package)
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

    # def get_packages_by_status(self, packages):
    #     packages_by_status = {}
    #     for package in packages:
    #         if package is not None:
    #             if package.delivery_status in packages_by_status:
    #                 packages_by_status[package.delivery_status].append(package)
    #             else:
    #                 packages_by_status[package.delivery_status] = []
    #                 packages_by_status[package.delivery_status].append(package)
    #     return packages_by_status
    #
    # def get_packages_by_address(self, packages):
    #     packages_by_address = {}
    #     for package in packages:
    #         if package is not None:
    #             if package.delivery_address in packages_by_address:
    #                 packages_by_address[package.delivery_address].append(package)
    #             else:
    #                 packages_by_address[package.delivery_address] = []
    #                 packages_by_address[package.delivery_address].append(package)
    #     return packages_by_address
    #
    # def get_packages_by_deadline(self, packages):
    #     packages_by_deadline = {}
    #     for package in packages:
    #         if package is not None:
    #             if package.delivery_deadline in packages_by_deadline:
    #                 packages_by_deadline[package.delivery_deadline].append(package)
    #             else:
    #                 packages_by_deadline[package.delivery_deadline] = []
    #                 packages_by_deadline[package.delivery_deadline].append(package)
    #     return packages_by_deadline
    #
    #
    # def get_packages_by_city(self, packages):
    #     packages_by_city = {}
    #     for package in packages:
    #         if package is not None:
    #             if package.delivery_city in packages_by_city:
    #                 packages_by_city[package.delivery_city].append(package)
    #             else:
    #                 packages_by_city[package.delivery_city] = []
    #                 packages_by_city[package.delivery_city].append(package)
    #     return packages_by_city
    #
    # def get_packages_by_zip(self, packages):
    #     packages_by_zip = {}
    #     for package in packages:
    #         if package is not None:
    #             if package.delivery_zip in packages_by_zip:
    #                 packages_by_zip[package.delivery_zip].append(package)
    #             else:
    #                 packages_by_zip[package.delivery_zip] = []
    #                 packages_by_zip[package.delivery_zip].append(package)
    #     return packages_by_zip
    #

    #
    # def get_packages_by_delayed(self, packages):
    #     packages_by_delayed = {}
    #     for package in packages:
    #         if package is not None:
    #             if package.delivery_zip in packages_by_delayed:
    #                 packages_by_delayed[package.delivery_zip].append(package)
    #             else:
    #                 packages_by_delayed[package.delayed] = []
    #                 packages_by_delayed[package.delayed].append(package)
    #     return packages_by_delayed
    #
    # def get_packages_by_required_truck(self, packages):
    #     packages_by_required_truck = {}
    #     for package in packages:
    #         if package is not None:
    #             if package.delivery_zip in packages_by_required_truck:
    #                 packages_by_required_truck[package.required_truck].append(package)
    #             else:
    #                 packages_by_required_truck[package.required_truck] = []
    #                 packages_by_required_truck[package.required_truck].append(package)
    #     return packages_by_required_truck

    # def get_packages_by_distance(self, packages):
    #     for package in packages:
    #         for v in

