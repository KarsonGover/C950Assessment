# This class is a chaining hash table for the packages
from collections import deque


class ChainingHashTable:
    def __init__(self, initialCapacity=40):
        self.table = []
        for i in range(initialCapacity):
            self.table.append([])

    def insert(self, key, item):
        # Reach the bucket's list where the key should be
        bucket = hash(key) % len(self.table)
        bucketList = self.table[bucket]

        for kv in bucketList:
            if kv[0] == key:
                kv[1] = item
                return True

        keyValue = [key, item]
        bucketList.append(keyValue)
        # print(bucketList)
        return True

    def search(self, key):
        # Reach the bucket's list where the key should be
        bucket = hash(key) % len(self.table)
        bucketList = self.table[bucket]
        # If the key is in the bucket's list, return the value
        # search for the key in the bucket list

        for kv in bucketList:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucketList = self.table[bucket]

        # remove the item from the bucket list if it is present
        for kv in bucketList:
            if kv[0] == key:
                bucketList.remove([kv[0], kv[1]])
