from datetime import datetime

# Represents a package with attributes for delivery information and status tracking.
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, special_notes=""):
        """ 
        Time Complexity: O(1) 
        Space Complexity: O(1)
        """
        self.package_id = int(package_id)
        self.correct_address = address
        self.address = address
        self.city = city
        self.state = state
        self.correct_zip_code = zip_code
        self.zip_code = zip_code
        self.deadline = deadline if deadline != "EOD" else "17:00"  # Handling "EOD"
        self.weight = weight
        self.special_notes = special_notes
        self.status = 'At the Hub'  # Default status
        self.delivery_time = None  # Time when the package is delivered
        self.available_time = None
        self.delay_until_time = None
        self.wrong_address_flag = False

        # Initializes a package object to handle special notes that might cause delays
        if "Delayed on flight" in special_notes:
            self.delay_until_time = "09:05"
        elif "Wrong address listed" in special_notes:
            self.delay_until_time = "10:20"
            self.wrong_address_flag = True
        if self.delay_until_time:
            self.available_time = datetime.strptime(self.delay_until_time, "%H:%M")

    def update_status(self, status, delivery_time=None):
        """
        Updates the status and delivery time of the package.

        Time Complexity: O(1)
        Space Complexity: O(1) 
        """
        self.status = status
        if delivery_time:
            self.delivery_time = datetime.strptime(delivery_time, "%H:%M:%S")

    def check_status_based_on_time(self, input_time, truck_start_time=None):
        """ 
        Updates the package status based on the input time and other special conditions.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        input_time = datetime.strptime(input_time, "%H:%M")
        truck_start_time_dt = datetime.strptime(truck_start_time, "%H:%M") if truck_start_time else None

        # WGUPS does not know the correct address for package #9 until 10:20
        if self.wrong_address_flag and input_time < datetime.strptime("10:20", "%H:%M"):
            # Make address and zip have placeholder values before 10:20
            self.address = "300 State St"
            self.zip_code = "84103"
        else:
            # Show correct address after 10:20
            self.address = self.correct_address
            self.zip_code = self.correct_zip_code

        # If delivery time AND time input are greater than delivery time, set status to 'DELIVERED AT '
        if self.delivery_time and input_time >= self.delivery_time:
            self.status = 'DELIVERED AT '
        # If not, then  if 'delay until time' AND the 'time input' are less than the time for 'delay until', set status to 'DELAYED UNTIL {delay until time}'
        elif self.delay_until_time and input_time < datetime.strptime(self.delay_until_time, "%H:%M"):
            self.status = f"DELAYED UNTIL {self.delay_until_time}"
        # If not, then if the 'truck start time' (dispatch time) AND the 'input time' are less than the 'truck start time', set status to 'AT THE HUB'
        elif truck_start_time_dt and input_time < truck_start_time_dt:
            self.status = 'AT THE HUB'
        # If none of the above, then set status to 'Out for Delivery'
        else:
            self.status = 'OUT FOR DELIVERY'

    def __str__(self):
        """ 
        Provides a string of the package info.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        delivery_time_str = self.delivery_time.strftime('%H:%M:%S') if self.delivery_time and self.status == 'DELIVERED AT ' else ''
        return (f"PACKAGE ID: {self.package_id} | {self.status}{delivery_time_str} | DEADLINE IS AT {self.deadline} | "
                f"ADDRESS: {self.address} | CITY: {self.city} | STATE: {self.state} | ZIP: {self.zip_code} | WEIGHT: {self.weight}kg")
