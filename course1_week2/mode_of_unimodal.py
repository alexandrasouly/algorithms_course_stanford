# Task:
# You are a given a unimodal array of n distinct elements,
# meaning that its entries are in increasing order up until its maximum element,
# after which its elements are in decreasing order.
# Give an algorithm to compute the maximum element that runs in O(log n) time.

# Solution:
# Divide and conquer - take 2 element at thirds and discard third where mode

import math


def find_mode(array):
    # base case
    if len(array) < 5:
        max = array[0]
        for i in array:
            max = i if i>max else max
        return max
    third = math.floor((len(array)+1)/3)
    left, right = array[third], array[2*third]
    if left < right:
        new_array = array[left:]
        return find_mode(new_array)
    else:
        new_array = array[:right]
        return find_mode(new_array)

if __name__=="__main__":
    array = [1,3,4,6,7,9,10,8,2,0]
    mode = find_mode(array)
    print(mode)
