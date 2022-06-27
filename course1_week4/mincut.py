# Task:
# Implement the Karger Minimum Cut algorithm.
# The input is an adjacency list representation of a simple undirected graph.
# As the algorithm isn't certain to find the minimum cut,
# please make sure to run the algorithm many times with different random seeds, 
# and remember the smallest cut that you ever find.

import math
from random import randint

def process_input():
    graph_dict = {}
    with open('course1_week4/input.txt') as f:
        for line in f.readlines():
            line = line.strip().split("\t")
            graph_dict[int(line[0])] = list(map(int,line[1:]))
    return graph_dict

def run_many_times(graph_dict):
    # This algorithm needs to be ran Ncr2 * log n times to succeed with a high probability
    n = len(graph_dict)
    min = n
    for _  in range(math.ceil(n*(n-1)/2*math.log(n))):
        min_cut = krager_min_cut(graph_dict)
        if min_cut< min:
            min = min_cut
    return min

class Graph:
    def __init__(self, graph) -> None:
        self.graph = graph.copy()
        edge_count = 0
        for edge_list in self.graph.values():
            edge_count += len(edge_list)
        self.edge_count = int(edge_count/2) # edges were counted twice
        self.vertex_count = len(self.graph.keys())

    def pick_random_edge(self):
        # We pick a random edge uniformly
        rand_edge = randint(0, self.edge_count-1)
        for vertex, edge_list in self.graph.items():
            if rand_edge >= len(edge_list):
                rand_edge -= len(edge_list)
            else:
                from_vertex = vertex
                to_vertex = edge_list[rand_edge]

                return from_vertex,to_vertex

    def collapse_edge(self, edge_from, edge_to):
        # we are removing edges between the two vertices that collapse
        edges_to_remove = self.graph[edge_from].count(edge_to)
        # the new edge will have all edges the two did
        # except the one between the two
        new_edge = self.graph[edge_from] +self.graph[edge_to]
        for _ in range(edges_to_remove):
            new_edge.remove(edge_to)
            new_edge.remove(edge_from)
        self.edge_count -= edges_to_remove
        # one fewer vertex since we make 1 out of 2
        self.vertex_count -= 1
        # we keep to "from" one, and change the pointers to the "to" one to it
        self.graph[edge_from] = new_edge
        self.graph.pop(edge_to)
        for key, edges in self.graph.items():
            self.graph[key] = [edge_from if value == edge_to else value for value in edges]

def krager_min_cut(graph_dict):
    graph = Graph(graph_dict)
    # we collapse until only two left
    while graph.vertex_count >2:
        edge_from, edge_to = graph.pick_random_edge()
        graph.collapse_edge(edge_from, edge_to)
    # the result is the edges between the last two
    # not necessarily the min cut though
    min_cut = graph.edge_count
    return min_cut

if __name__=="__main__":
    graph_dict = process_input()
    min_cut = run_many_times(graph_dict)
    print(min_cut)