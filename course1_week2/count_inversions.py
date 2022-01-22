# Task:
# The input file contains all of the 100,000 integers between
# 1 and 100,000 (inclusive) in some order, with no integer repeated.
# Your task is to compute the number of inversions in the file given, where the i^{th}
# row of the file indicates the i^{th} entry of an array.
# You should implement a fast divide-and-conquer algorithm.

def process_input():
    with open('course1_week2/integers.txt') as f:
        array = list(map(int, f.readlines()))
    return array

def count_inversions(array):
    # Base case
    if len(array) ==1:
        return 0, array
    else:
        # Divide in half, and check both halves
        left_half = array[:int(len(array)/2)]
        right_half =  array[int(len(array)/2):]
        left_inversions, sorted_left_half = count_inversions(left_half)
        right_inversions, sorted_right_half = count_inversions(right_half)
        # Count whether there are inversions s.t. one if in left, other in right
        # We sort the array in this step and count during merge sort
        split_inversions, sorted_array = count_split_inversions(sorted_left_half, sorted_right_half)
        return (left_inversions+ right_inversions+ split_inversions), sorted_array

def count_split_inversions(sorted_left_half, sorted_right_half):
    split_inversions = 0
    i = 0
    j = 0
    sorted_array = []
    sorted_array_len = len(sorted_left_half) + len(sorted_right_half)
    # Merge sort, when copying from the right we have inversions with
    # everything left in the left half
    for _ in range(sorted_array_len):
        if j>=len(sorted_right_half) or ( i<len(sorted_left_half) and sorted_left_half[i] < sorted_right_half[j]):
            sorted_array.append(sorted_left_half[i])
            i +=1
        elif i>=len(sorted_left_half) or (j<len(sorted_right_half)) and sorted_left_half[i] > sorted_right_half[j]:
            sorted_array.append(sorted_right_half[j])
            split_inversions += len(sorted_left_half) - i
            j +=1

    return split_inversions, sorted_array

if __name__=="__main__":
    array = process_input()
    split_inversions, _ = count_inversions(array)
    print(split_inversions)
