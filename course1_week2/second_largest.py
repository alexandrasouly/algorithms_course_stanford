# Task:
# You are given as input an unsorted array of n distinct numbers, where n is a power of 2.
# Give an algorithm that identifies the
# second-largest number in the array, and that uses at most n +log_2 n - 2 comparisons.

# Get maximum element by building a tournament tree/winning tree max heap with n-1 comparisons
# Get largest one that lost to the max in the tree - this is at most log_2 n -1 steps


def process_input():
    with open('course1_week2/1024_ints.txt') as f:
        array = list(map(int, f.readlines()))
    return array

class Node:
    def __init__(self, data):
        self.size =1
        self.left = None
        self.right = None
        self.data = data

    def display(self):
        # prints tree from the bottom left
        if self.left:
            self.left.display()
        if self.data:
            print(self.data)
        if self.right:
            self.right.display()


def build_tournament_tree(array):
    """ Build a turnament tree using n-1 comparisons"""
    # building first level
    nodes = [Node(data) for data in array]
    # build until one node, which is the whole tree
    while len(nodes) != 1:
        new_nodes = []
        for i in range(0, len(nodes), 2):
            (bigger,smaller) = (nodes[i], nodes[i+1]) if nodes[i].data> nodes[i+1].data else (nodes[i+1], nodes[i])
            root = Node(bigger.data)
            root.left = bigger
            root.right = smaller
            root.size = root.left.size+root.right.size+1
            new_nodes.append(root)
        nodes = new_nodes
    return nodes[0]

def get_second_best(tree):
    """ Get second best using log_2 n - 1 comparisons"""
    current_node = tree
    fought_max = []
    # get to level before leaves
    while current_node.left is not None:
        fought_max.append(current_node.right.data)
        current_node = current_node.left # we constructed our tree st the left on is the max
    second_best = fought_max[0]
    print(fought_max)
    for i in range(1, len(fought_max)):
        second_best = fought_max[i] if fought_max[i] > second_best else second_best
    return second_best


if __name__=="__main__":
    array = process_input()
    tree = build_tournament_tree(array)
    print(get_second_best(tree))
