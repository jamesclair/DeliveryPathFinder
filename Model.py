
class Package:

    def __init__(self, package_id, package_weight, special_note, delivery_address, delivery_city, delivery_zip, delivery_deadline):
        self.package_id = package_weight
        self.package_weight = package_weight
        self.special_note = special_note
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline  # TODO: Not sure how to handle time type without imports yet.  May NOT be required.


class Truck:

    def __init__(self):
        self.MAX_LOAD = 16
        self.load = HashTable(self.MAX_LOAD)  # Assumption:
        self.AVG_MPH = 18
        self.start_time = 8
        self.DELIVERY_TIME_SECONDS = 0.0


class HashTable:
    def __init__(self, size = 0):
        self.table = []
        for i in range(size):
            self.table.append([])

    def insert(self, item):
        bucket = hash(item) % len(self.table)
        bucket_list = self.table[bucket]

        bucket_list.append(item)

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            bucket_list.remove(key)
