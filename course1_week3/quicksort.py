# Task:
# Your task is to compute the total number of comparisons used
# to sort the given input file by QuickSort.
# As you know, the number of comparisons depends on which elements
# are chosen as pivots, so we'll ask you to explore three different pivoting rules.
# For the first part of the programming assignment, you should always use the first
# element of the array as the pivot element.
# Next, using the final element of the given array as the pivot element.
# Finally, consider the first, middle, and final elements of the given array.
# Compute the number of comparisons using the "median-of-three" pivot rule.

import math

def process_input():
    with open('course1_week2/integers.txt') as f:
        array = list(map(int, f.readlines()))
    return array

def quicksort(array, pivot_type, start, end, comparison_counter=0):
    comparison_counter += end-start
    # base case
    if end-start<=1:
        if array[end]< array[start]:
            array[end], array[start] = array[start], array[end]
        return array,comparison_counter
    # a recursive call was called, this is array_length-1 comparisons
    # pick pivot based on specified method
    pivot_idx, pivot = pick_pivot(array, pivot_type,start, end)
    # put pivot at the beginning
    array[start], array[pivot_idx] = array[pivot_idx], array[start]
    # boundary is where numbers start to be bigger than pivot
    # meaning array[boundary] will be the one after the pivot
    # when we find more smaller number, this gets pushed out
    boundary = start+1
    for i in range(start+1,end+1):
        if array[i]< pivot:
            array[i], array[boundary] = array[boundary], array[i]
            boundary+=1
    # switch pivot back
    array[boundary-1], array[start] = array[start], array[boundary-1]
    if boundary-2 > start: # pivot wasn't the smallest item, sort left to it
        # we don't want to include the pivot in the sort hence boundary-2 for end
        array, comparison_counter = quicksort(array, pivot_type, start, boundary-2, comparison_counter)
    if boundary < end:  # pivot wasn't the biggest item, sort right to it
        array, comparison_counter = quicksort(array, pivot_type, boundary, end, comparison_counter)
    return array,comparison_counter



def pick_pivot(array,pivot_type, start, end):
    """ Picks pivot according to the method we choose"""
    if pivot_type == "first":
        pivot_idx, pivot = start, array[start]
    if pivot_type == "last":
        pivot_idx, pivot = end, array[end]
    if pivot_type == "median":
        pivot_idx, pivot = median_of_three(array, start, end)
    return pivot_idx, pivot

def median_of_three(array, start, end):
    """
    Takes two element in an array, finds the one halfway in the middle
    and returns the median of these three
    """
    first_idx, first = start, array[start]
    middle_idx, middle  = math.floor((start+end)/2), array[math.floor((start+end)/2)]
    last_idx, last = end, array[end]

    if first < middle < last or first > middle > last:
        return middle_idx, middle
    elif middle < first < last or middle > first > last:
        return first_idx, first
    elif middle < last < first or middle > last > first:
        return last_idx, last


if __name__=="__main__":
    array = process_input()
    _,comparisons = quicksort(array, "first", 0, len(array)-1)
    print("With the pivot as first element, the number of comparisons:")
    print(comparisons)

    array = process_input()
    _,comparisons = quicksort(array, "last", 0, len(array)-1)
    print("With the pivot as last element, the number of comparisons:")
    print(comparisons)

    array = process_input()
    _,comparisons = quicksort(array, "median",  0, len(array)-1)
    print("With the pivot as median of three elements, the number of comparisons:")
    print(comparisons)
