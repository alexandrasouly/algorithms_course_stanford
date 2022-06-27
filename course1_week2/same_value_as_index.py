# Task:
# You are given a sorted (from smallest to largest) array A of n distinct integers
# which can be positive, negative, or zero.
# You want to decide whether or not there is an index i such that A[i] = i.
# Design the fastest algorithm that you can for solving this problem.

# Solution:
# Using a divide and conquer approach, there is an O(logn) solution.

import math


def find_value_as_index(starting_index, array):
    # Starting index shows where in the original array
    # is our current array starting.
    # This is helpful to convert what value should match what index.

    # base case
    if len(array) ==1:
        if array[0] == starting_index:
            return True
        else:
            return False

    middle = math.floor(len(array)/2)
    if array[middle] < starting_index+middle:
        # we discard first half as there can't be any there
        return find_value_as_index(starting_index+middle, array[middle:])
    elif array[middle] == starting_index+middle:
        # yay found it
        return True
    else:
        # we discard second half as there can't be any there
        return find_value_as_index(starting_index+middle, array[:middle])

if __name__=="__main__":
    array = [-5,-2,-1,0,4,5,6,7,9,10]
    mode = find_value_as_index(0,array)
    print(mode)
