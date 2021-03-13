import Time
from Location import Location
class Package:

    def __init__(self, package_id, package_weight, special_note, delivery_address, delivery_city, delivery_zip,
                 delivery_deadline, delivery_state):
        self.package_id = package_id
        self.package_weight = package_weight
        self.special_note = special_note
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.priority = False
        self.delivery_state = delivery_state
        self.delivery_time = 0
        self.delivery_status = 'hub'
        self.truck_id = 0
        self.is_wrong_addr = False
        self.peer_packages = []
        self.arrival_time = 0
        self.location = Location(None)
        self.delayed = False
        self.required_truck = 0
        self.delivery_weight = 0
        self.is_correct = True
        self.is_special = False

    def __str__(self):
        return ('Package Id: ' + self.package_id.__str__()
                + '\nTruck ID: ' + self.truck_id.__str__()
                + '\nStatus: ' + self.delivery_status.__str__()
                + '\nSpecial Note: ' + self.special_note.__str__()
                + '\nDelivery Address: ' + self.delivery_address.__str__() + ', ' + self.delivery_city.__str__() + ', '
                                         + self.delivery_state.__str__() + ', ' + self.delivery_zip.__str__()
                + '\nDelivery Deadline: ' + self.delivery_deadline.__str__()
                + '\nArrival Time: ' + Time.get_formatted_time(self.arrival_time)
                + '\nPeer Packages: ' + self.peer_packages.__str__()
                + '\nLocation: ' + self.location.label.__str__() + ', Distance: ' + self.location.distance.__str__()
                + '\n\n'
                )

    def deliver_package(self, time):
        self.arrival_time = time
        self.delivery_status = 'delivered'
