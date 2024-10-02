# A basic implementation of a hash table using separate chaining for collision resolution.
class HashTable:
    def __init__(self, size=20):
        """
        Initializes the hash table with a specified size (number of buckets).

        Time Complexity: O(1)
        Space Complexity: O(n)
        """

        self.size = size
        self.table = [[] for _ in range(self.size)]  

    def _hash(self, key):
        """
        Calculates the hash value for a given key. 
        Uses a simple modulo operation.

        Returns the calculated hash value (bucket index).

        Time Complexity: O(1) 
        Space Complexity: O(1)  
        """

        return key % self.size
    
    def insert(self, package_id, data):
        """
        Inserts a new package (key-value pair) into the hash table.

        Time Complexity:
            * Average Case: O(1)
            * Worst Case: O(n) - If all items hash to the same bucket, degrades to linear search.  

        Space Complexity: O(1)
        """

        hash_index = self._hash(package_id)

        # Check for existing entry and update 
        for i, (k, _) in enumerate(self.table[hash_index]):
            if k == package_id:
                self.table[hash_index][i] = (package_id, data)
                return

        # If not found, append 
        self.table[hash_index].append((package_id, data))

    def lookup(self, package_id):
        """
        Retrieves the data associated with a package ID.

        Returns the package data if found, else None.

        Time Complexity:
            * Average Case: O(1) 
            * Worst Case: O(n) - If all items hash to the same bucket, degrades to linear search.  

        Space Complexity: O(1) 
        """

        hash_index = self._hash(package_id)
        for k, v in self.table[hash_index]:
            if k == package_id:
                return v
        return None
