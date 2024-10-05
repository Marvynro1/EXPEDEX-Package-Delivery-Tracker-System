import re

# Represents the CLI for the EXPEDEX package delivery system.
class CLI:
    def __init__(self, trucks, package_table, distance_manager):
        """
        Initializes the CLI with trucks, package table, and distance information.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """

        self.trucks = trucks
        self.package_table = package_table
        self.distance_manager = distance_manager

    def run(self):
        """
        Main loop of the CLI, handling user interaction.

        Time Complexity: O(n)
        Space Complexity: O(1)  
        """

        while True:
            self.display_main_menu()
            choice = input("\nenter your choice: ")
            if choice == '1':
                self.check_status()
            elif choice == '2':
                break # Exit the program
            else:
                print("Invalid option, please try again.")

    def display_main_menu(self):
        """
        Displays the main menu and calculates total miles.

        Time Complexity: O(n)
        Space Complexity: O(1) 
        """

        total_miles = sum(truck.total_miles for truck in self.trucks)
        print("*************************************")
        print("****** EXPEDEX PACKAGE TRACKER ******")
        print("*************************************")
        # Print the time the truck returns to the hub
        print(f"Total miles driven (including drive back to hub): {total_miles:.2f}")
        print ("\nStatus ouput for `all` will show the optimized route as a list for each truck.")
        print("\n1. Check Status\n2. Exit")

    def check_status(self):
        """
        Handles user input for checking package statuses (single or all).

        Time Complexity: O(n^2) in the worst case
        Space Complexity: O(1)
        """

        time_str = input("Enter Time (HH:MM): ")
        # Validate time format using regular expression
        if not re.match(r'^\d{2}:\d{2}$', time_str):
            print("Invalid input. Please enter a time (HH:MM).")
            return  # Return to the main menu if the input is invalid
        
        choice = input("Check Single Package or All? (Enter 'single' or 'all'): ")

        if choice.lower() == 'single':
            package_id = int(input("Enter ID: "))
            package = self.package_table.lookup(package_id)
            if package:
                # Find the truck for this package
                for truck in self.trucks:
                    if package_id in truck.packages:
                        # Pass the truck's start time to the package status check
                        package.check_status_based_on_time(time_str, truck.start_time.strftime('%H:%M'))
                        print(f"\nTruck #{truck.truck_id} (Dispatches at {truck.start_time.strftime('%H:%M')}):")
                        print(package)
                        break
            else:
                print(f"Package with ID {package_id} not found.")
        elif choice.lower() == 'all':
            for truck in self.trucks:
                print(f"\nTruck #{truck.truck_id} (Dispatches at {truck.start_time.strftime('%H:%M')}):")
                for package_id in truck.packages:
                    package = self.package_table.lookup(package_id)
                    if package:
                        # Pass the truck's start time for each package
                        package.check_status_based_on_time(time_str, truck.start_time.strftime('%H:%M'))
                        print(package)
        else:
            print("Invalid option, returning to main menu.")

