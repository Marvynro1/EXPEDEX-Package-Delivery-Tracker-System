from datetime import datetime, timedelta

# Represents a delivery truck responsible for making deliveries of assigned packages.
class Truck:
    def __init__(self, truck_id, packages, address_mapping, distance_manager, package_table, start_time):
        """
        Initializes a truck with its attributes.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        self.truck_id = truck_id
        self.packages = packages
        self.address_mapping = address_mapping
        self.distance_manager = distance_manager
        self.package_table = package_table
        self.start_time = datetime.strptime(start_time, "%H:%M")
        self.total_miles = 0
        self.current_time = self.start_time  # Initialize current time as the start time

    def dispatch(self):
        """
        Conducts the delivery process using the nearest neighbor algorithm and updates package statuses.

        Time Complexity: O(n^2)
        Space Complexity: O(n)
        """

        current_location_index = self.address_mapping['4001 South 700 East']  # Hub address index
        package_indices = [self.address_mapping[self.package_table.lookup(package_id).address] for package_id in self.packages]
        
        # Optimize route using Nearest Neighbor Algorithm from DistanceManager
        optimized_route, total_distance = self.distance_manager.calculate_route(current_location_index, package_indices)
        self.total_miles += total_distance

        # Update the order of packages based on the optimized route
        optimized_package_order = []
        assigned_packages = set()  # Keep track of which packages have been assigned to prevent duplicates

        for destination_index in optimized_route:
            for package_id in self.packages:
                if package_id in assigned_packages:
                    continue  # Skip this package if it has already been assigned
                
                package = self.package_table.lookup(package_id)
                if package and self.address_mapping[package.address] == destination_index:
                    optimized_package_order.append(package_id)
                    assigned_packages.add(package_id)  # Mark this package as assigned
                    break  # Move to the next destination in the optimized route

        self.packages = optimized_package_order  # Update the package list with the optimized order

        # Make Delivery and Update Statuses     
        for destination_index in optimized_route:
            for package_id in self.packages:
                package = self.package_table.lookup(package_id)
                if package and self.address_mapping[package.address] == destination_index:
                    distance = self.distance_manager.calculate_distance(current_location_index, destination_index)
                    travel_time = timedelta(hours=distance / 18)  # 18 mph average speed
                    self.current_time += travel_time  # Update current time based on travel
                    # Update package status to 'Delivered' with current_time
                    if package.status != 'Delivered':
                        package.update_status('Delivered', self.current_time.strftime("%H:%M:%S"))
                    current_location_index = destination_index  # Update current location to this package's destination                    

        # Distance to return to hub
        hub_distance = self.distance_manager.calculate_distance(current_location_index, self.address_mapping['4001 South 700 East'])
        travel_time_back = timedelta(hours=hub_distance / 18)
        self.current_time += travel_time_back
        self.total_miles += hub_distance

        # Print the time the truck returns to the hub
        print(f"Truck {self.truck_id} dispatched at {self.start_time.strftime('%H:%M')} and returned to the hub at {self.current_time.strftime('%H:%M:%S')}.")