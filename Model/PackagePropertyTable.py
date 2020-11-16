class PackagePropertyTable:

    def __init__(self, size):
        self.table = []
        self.keys = []
        for i in range(size):
            self.table.append([])

    def create(self, key, value):
        # key = int(key)
        bucket = hash(key) % len(self.table)
        self.table[bucket].append(value)
        self.keys.append(key)

    def read(self, key):
        # key = int(key)
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        if len(bucket_list) > 0:
            return bucket_list
        else:
            return None

    def delete(self, key):
        # key = int(key)
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if bucket in bucket_list:
            bucket_list.remove(bucket)

