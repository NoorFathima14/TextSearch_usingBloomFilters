import hashlib
import sys
import math
import time
from bitarray import bitarray

class BloomFilter:
    def __init__(self, bit_array_size, false_positive_probability, num_elements):
        self.size = bit_array_size
        self.probability = false_positive_probability
        self.num_elements = num_elements
        self.num_hashes = 1
        if num_elements != 0:
            self.num_hashes = int((bit_array_size / num_elements) * (math.log10(2)))
        self.bit_array = bitarray('0' * int(bit_array_size))

    def hash_sha256(self, item):
        encoded = hashlib.sha256(item.encode())
        return int(encoded.hexdigest(), base=16) % self.size
    '''
    def hash_md5(self, item):
        encoded = hashlib.md5(item.encode())
        return int(encoded.hexdigest(), base=16)

    def hash_sha512(self, item):
        encoded = hashlib.sha512(item.encode())
        return int(encoded.hexdigest(), base=16)
    '''
    def calculate_false_positive_probability(self, bit_array_size, num_elements):
        return 0.5 ** (math.log10(2)) * (bit_array_size / num_elements)

    def insert(self, item):
        for count in range(self.num_hashes):
            index = int(self.hash_sha256(item + str(count)) % self.size)
            self.bit_array[index] = 1

    def lookup(self, item):
        for count in range(self.num_hashes):
            check = int(self.hash_sha256(item + str(count)) % self.size)
            if self.bit_array[check] == 0:
                return False
        return True

def binary_search(search_data, target, data_length):
    first = 0
    last = data_length - 1
    while first <= last:
        mid = (first + last) // 2
        middle_item = search_data[mid]
        if middle_item < target:
            first = mid + 1
        elif middle_item > target:
            last = mid - 1
        else:
            return middle_item
    return False

def insert_items(bloom_filter, items):
    for item in items:
        bloom_filter.insert(item)

        
print("\n\n------------------- TEXT SEARCH ENGINE -------------------\n\n")
        
with open('testtxtdox.txt', encoding='ISO_8859-1') as loaded_file:
    loaded_data = loaded_file.read().split()

user_input = input("Enter a word to check (case sensitive): ")
user_input = user_input.encode('utf-8').decode('ISO_8859-1')

num_loaded_elements = len(loaded_data)
desired_false_positive_probability = 0.01
bit_array_size = int(-(num_loaded_elements * math.log10(desired_false_positive_probability)) / (math.log10(2) ** 2))
bloom_filter = BloomFilter(bit_array_size, desired_false_positive_probability, num_loaded_elements)

insert_items(bloom_filter, loaded_data)



if bloom_filter.lookup(user_input):
    print("The word is in the document (possibly a true positive).")
else:
    print("The word is not in the document (false positive or true negative).")
    
print("_____________________________________________________________")
print("| Number of elements added (n):",bloom_filter.num_elements)
print("| Size of bit array (m):",bloom_filter.size)
print("| Probability of false positives (p):",bloom_filter.probability)
print("| Number of hash functions used (k):",bloom_filter.num_hashes)
print("=============================================================")


#validating
print("\n\n...checking if input data exists...")

file_name = 'testtxtdox.txt'

with open(file_name, 'r') as input_file:
    data = input_file.read().split()
                                  
check_neg = []
check_pos = []

for item in data:
    result = bloom_filter.lookup(item)
    if result is False:
        check_neg.append(item)
        print("no")
    else:
        check_pos.append(item)
        print("maybe")
print("...done checking input data...")
print("...validating results...")

true_negatives = 0
false_negatives = 0
false_positives = 0
true_positives = 0

check_neg.sort()
check_pos.sort()

for item in check_neg:
    result = binary_search(loaded_data, item, len(loaded_data))
    if result is False:
        true_negatives += 1
    else:
        false_negatives += 1

for item in check_pos:
    result = binary_search(loaded_data, item, len(loaded_data))
    if result is False:
        false_positives += 1
    else:
        true_positives += 1

end_time = time.time()

print("| RESULTS:")
print("|========")
print("| True Negatives:",true_negatives)
print("| False Negatives:",false_negatives)
print("| True Positives:",true_positives)
print("| False Positives:",false_positives)
print("_____________________________________________________________")
 

if (false_positives + true_negatives) == 0:
    actual_false_positive_rate = 0
else:
    actual_false_positive_rate = false_positives / (false_positives + true_negatives)

print("_____________________________________________________________")
print("~ False Positive Rate: ", actual_false_positive_rate)
print("_____________________________________________________________")
