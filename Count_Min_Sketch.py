import numpy as np
import random

from heapq import heappush, heappop, heapify


# class for pair-wise hash functions
class HashFunction:
    def __init__(self, hash_range, p):
        self.w = hash_range  # number of range of the hash functions
        # hash function coefficient
        # choose hash coefficients according within the range
        self.a = random.randint(1, p - 1)
        self.b = random.randint(0, p - 1)
        self.p = p

    def hash(self, item):  # get hash value within w slots
        hash_value = hash(item)

        return (((self.a * hash_value) + self.b) % self.p) % self.w


class CountMinSketch:
    def __init__(self, w, d, p):
        self.hash_functions = []
        for i in range(d):  # we need d hash functions
            self.hash_functions.append(HashFunction(w, p))  # generate hash functions
        self.count_min_sketches = np.zeros((d, w))  # get the sketch with all zeros

    def update(self, item):  # update the sketch
        for index, hash_function in enumerate(self.hash_functions):  # for each hash function
            self.count_min_sketches[index][hash_function.hash(item)] += 1  # increase the sketch accordingly

    def get(self, item):  # query the frequency of a specific item
        minimum = float("inf")
        for index, hash_function in enumerate(self.hash_functions):  # find the minimum value
            current_frequency = self.count_min_sketches[index][hash_function.hash(item)]
            if current_frequency < minimum:
                minimum = current_frequency

        return minimum


# find the nearest prime number which is greather than m to construct the pair-wise hash functions
def find_prime(num):
    while True:
        prime = True
        for j in range(2, int(num ** (1 / 2)) + 1):
            if num % j == 0:
                prime = False
                break
        if prime:
            return num

        num += 1


def heap_deletion(m, k, heap):
    temp_dict = {}
    # go over the heap takes O(k)
    for count, tag in heap:
        if count < (m / k):  # if the frequency is less
            continue  # we skip this item in the heap

        if tag in temp_dict:  # if this is a tag seen before & frequency greater than the threshold
            if count > temp_dict[tag][0]:  # if we got a larger frequency
                temp_dict[tag] = (count, tag)  # update the frequency
        else:  # if this is a new tag with frequency greater than the threshold
            temp_dict[tag] = (count, tag)  # store the it

    # after go over the heap, we got all unique tag with highest frequencies
    # we can just construct a new heap with these items
    output_heap = []
    # takes O(klogk)
    for tag in temp_dict:  # this takes O(k)
        heappush(output_heap, temp_dict[tag])  # each push use O(logk)

    return output_heap


# we do not actually use this for the home work
class PriorityQueue(object):  # min heap for vanilla implementation not for the homework
    def __init__(self):
        self.pq = []
        self.item_map = {}

    def __len__(self):
        return len(self.pq)

    def push(self, item, count):
        self.remove(item)

        entry = (count, item)
        self.item_map[item] = entry

        heappush(self.pq, entry)

    def remove(self, item):  # delete previous occurrence
        if item in self.item_map:
            entry = self.item_map.pop(item)
            self.pq.remove(entry)
            heapify(self.pq)

    def pop(self):
        count, item = heappop(self.pq)
        del self.item_map[item]
        return count, item
