"""
Name: Marvyn Orellana
Student ID: 010291805
"""

import csv
from hash_table import HashTable
from truck import Truck
from package import Package
from distance import DistanceManager
from cli import CLI

def load_address_mapping(filename="Data_Files/Address.csv"):
    """
    Loads the address mapping from a CSV file.

    Returns a dictionary mapping addresses (strings) to their indices (integers).

    Time Complexity: O(n)
    Space Complexity: O(n) for address mapping dictionary
    """

    address_mapping = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        # Loops through the rows of the CSV
        for row in reader:
            index, _, address = row # Unpack values from the row
            address_mapping[address] = int(index) # Store address as the key and index as the value in dictionary
    return address_mapping

def load_distance_matrix(filename="Data_Files/Distance_Matrix.csv"):
    """
    Loads the distance matrix from a CSV file.

    Returns a 2D list representing distances between addresses.

    Time Complexity: O(n^2)
    Space Complexity: O(n^2) for distance matrix list
    """

    distance_matrix = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        # Loops though all elements in distance matrix
        for row in reader:
            distance_matrix.append([float(dist) for dist in row]) # Convert string distances to float
    return distance_matrix

def load_packages(filename="Data_Files/Package.csv", hash_table_size=40):
    """
    Loads packages from a CSV file and inserts them into a hash table.

    For efficient storage and quick retrieval by package ID.
    
    Returns a HashTable object containing the loaded packages.

    Time Complexity: O(n), for insertions O(1)
    Space Complexity: O(n)
    """

    package_table = HashTable(size=hash_table_size)
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        # Loops through the rows of the CSV
        for row in reader:
            package_id = int(row[0]) # Convert first element in row to integer
            package = Package(*row) # Create package object using raw data 
            package_table.insert(package_id, package) # Insert into hash table
    return package_table

def dispatch(trucks):
    """
    Calls the dispatch function of each truck to start deliveries.

    Time Complexity: O(n^2)
    Space Complexity: O(n)
    """

    for truck in trucks:
        truck.dispatch()

def main():
    """
    The main function to coordinate package delivery. Here is the overall flow:
    1. Loads data from CSV files.
    2. Dispatches trucks with optimized delivery routes.
    3. Initializes and starts the command-line interface (CLI).    

    Time Complexity: O(n^2)
    Space Complexity: O(n^2)
    """

    address_mapping = load_address_mapping("Data_Files/Address.csv")
    distance_matrix = load_distance_matrix("Data_Files/Distance_Matrix.csv")
    package_table = load_packages("Data_Files/Package.csv")
    distance_manager = DistanceManager(distance_matrix, address_mapping)

    # Pre-specified package lists for each truck
    truck1_packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
    truck2_packages = [3, 9, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]
    truck3_packages = [2, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33]

    trucks = [
    Truck(1, truck1_packages, address_mapping, distance_manager, package_table, "08:00"),
    Truck(2, truck2_packages, address_mapping, distance_manager, package_table, "10:20"),
    Truck(3, truck3_packages, address_mapping, distance_manager, package_table, "09:05"),
    ]

    dispatch(trucks)

    # Initialize CLI with trucks, package_table, and distance_manager
    cli_instance = CLI(trucks, package_table, distance_manager)
    cli_instance.run()  # Start the CLI interaction

if __name__ == "__main__":
    main()
