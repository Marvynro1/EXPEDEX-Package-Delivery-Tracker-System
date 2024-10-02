# Manages distance calculations and route optimization based on a preloaded distance matrix.
class DistanceManager:
    def __init__(self, distance_matrix, address_mapping):
        """
        Initializes the DistanceManager.

        Time Complexity: O(1)
        Space Complexity: O(n^2)
        """

        self.distance_matrix = distance_matrix
        self.address_mapping = address_mapping

    def calculate_distance(self, from_address_index, to_address_index):
        """
        Retrieves the distance between two addresses directly from the distance matrix.

        Returns the distance between the two addresses.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """

        return self.distance_matrix[from_address_index][to_address_index]

    def find_nearest_neighbor(self, current_location_index, unvisited_indices):
        """
        Finds the nearest unvisited address to the current location.

        Returns a tuple containing:
                * The index of the nearest unvisited address.
                * The distance to the nearest unvisited address.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """

        nearest_index = None
        shortest_distance = float('inf')
        # Loops through the list of unvisited addresses (indexes) and compares distances
        for index in unvisited_indices:
            distance = self.calculate_distance(current_location_index, index)
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_index = index
        return nearest_index, shortest_distance

    def calculate_route(self, current_location_index, package_indices):
        """
        Calculates a delivery route using the nearest neighbor algorithm.

        Returns a tuple containing: 
        * A list of indices representing the optimized delivery route.
        * The total distance of the route. 

        Time Complexity: O(n^2)
        Space Complexity: O(n)
        """

        unvisited_indices = package_indices[:]
        route = []
        total_distance = 0

        # While there are unvisited indices, continues to find the nearest unvisited address
        while unvisited_indices:
            nearest_index, distance = self.find_nearest_neighbor(current_location_index, unvisited_indices)
            route.append(nearest_index)
            total_distance += distance
            current_location_index = nearest_index
            unvisited_indices.remove(nearest_index)

        return route, total_distance
