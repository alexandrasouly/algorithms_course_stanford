# The input file contains the edges of a directed graph.
# Every row indicates an edge, the vertex label in first column is
# the tail and the vertex label in second column is the head.

# Your task is to code up the algorithm for computing strongly connected components (SCCs),
# and to run this algorithm on the given graph.
# You should output the sizes of the 5 largest SCCs in the given graph.


# Solution:
# We will implement Kosaraju's Two-pass algorithm
# First pass of DFS on the graph to record finishing times
# Second pass of DFS with nodes in reverse order of finishing times

import threading
from typing import List
import sys

def process_input():
    """ Read edges into a list of tuples"""
    edges = []
    with open('course2_week1/input.txt') as f:
        for line in f.readlines():
            line = line.strip().split(" ")
            edges.append((int(line[0]),int(line[1])))
    return edges

class Graph():
    def __init__(self, edges) -> None:
        """
        Storing info of the graph:
        edges - the list of tuples of the directed edges
        explored - a dictionary of node: bool whether we explored that edge in dfs
        finishing_time - an array of the order the nodes finished in dfs
        nodes_finished - number of nodes that finished in dfs
        edges_dict - a dict of node:[outgoing edges]
        reversed_edges_dict - a dict of node:[outgoing edges] for the reverse of the graph (all edges reversed)
        sccs - a list of strongly connected components
        """
        self.edges = edges
        # create dict with all nodes with values set as False
        self.explored = {start : False for (start,_) in self.edges}
        self.explored.update({end : False for (_,end) in self.edges})
        # this is the order the nodes finished in
        self.finishing_time = [None] * len(self.explored)
        self.nodes_finished = 0
        self.edges_dict = self.edges_from()
        self.reversed_edges_dict = self.edges_from(reversed= True)
        self.sccs: List[List[int]] = []


    def reset_explored(self):
        # reset explored nodes to none between first and second pass
        self.explored = {start : False for (start,_) in self.edges}
        self.explored.update({end : False for (_,end) in self.edges})

    def edges_from(self, reversed = False):
        # get dictionary of node:[out edges]
        # if reverse is true, it will do so for the reverse graph
        edges_from = {}
        for (start, end) in self.edges:
            if reversed: # we want the reverse graph, so just switch edge direction
                start, end = end, start
            if start not in edges_from:
                edges_from[start] = []
            if end not in edges_from:
                edges_from[end] = []
            edges_from[start].append(end)

        return edges_from

def first_pass(graph: Graph):
    # go through all nodes, set finishing times
    for node in graph.reversed_edges_dict.keys():
        if not graph.explored[node]:
           graph = first_pass_dfs(graph, node)
    return graph

def first_pass_dfs(graph:Graph, node):
    # first dfs pass on reverse dfs graph, record finish times
    graph.explored[node] = True
    for end_point in graph.reversed_edges_dict[node]:
        if not graph.explored[end_point]:
            graph.explored[end_point] = True
            first_pass_dfs(graph, end_point)
    graph.nodes_finished +=1
    graph.finishing_time[graph.nodes_finished-1]= node
    return graph


def second_pass(graph: Graph):
    # go through all nodes in decreasing finishing time order
    # record sccs
    # because of the magic of the starting points for dfs here, 
    # all the scc and only it wil be discovered in each call
    for node in graph.finishing_time[::-1]:
        if not graph.explored[node]:
           nodes_explored =[node]
           graph, nodes_explored = second_pass_dfs(graph, node, nodes_explored)
           graph.sccs.append(nodes_explored)
    return graph

def second_pass_dfs(graph:Graph, node, nodes_explored):
    # record nodes that we met in that in this call
    # all part of the same scc
    graph.explored[node] = True
    for end_point in graph.edges_dict[node]:
        if not graph.explored[end_point]:
            graph.explored[end_point] = True
            nodes_explored.append(end_point)
            second_pass_dfs(graph, end_point, nodes_explored)
    return graph, nodes_explored


def biggest_sccs(graph: Graph, top_sizes=5):
    # het 5 biggest sccs
    scc_lengths = list(map(lambda x: len(x), graph.sccs))
    return sorted(scc_lengths)[-top_sizes:]


def main():
    edges = process_input()
    graph = Graph(edges)
    graph = first_pass(graph)
    graph.reset_explored()
    graph = second_pass(graph)
    top_5_scc = biggest_sccs(graph)
    print(top_5_scc)


if __name__=="__main__":
    # avoiding recursion limit and segmentation fault
    threading.stack_size(67108864)
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=main)
    thread.start()