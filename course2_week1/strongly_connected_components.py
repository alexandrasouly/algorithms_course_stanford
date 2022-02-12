import threading
from typing import List
import sys

def process_input():
    edges = []
    with open('course2_week1/small_test_5.txt') as f:
        for line in f.readlines():
            line = line.strip().split(" ")
            edges.append((int(line[0]),int(line[1])))
    return edges

class Graph():
    def __init__(self, edges) -> None:
        self.edges = edges
        self.explored = {start : False for (start,_) in self.edges}
        self.explored.update({end : False for (_,end) in self.edges})
        # this is the order the nodes finished in
        self.finishing_time = [None] * len(self.explored)
        self.nodes_finished = 0
        self.edges_dict = self.edges_from()
        self.reversed_edges_dict = self.edges_from(reversed= True)
        self.sccs: List[List[int]] = []


    def reset_explored(self):
        self.explored = {start : False for (start,_) in self.edges}
        self.explored.update({end : False for (_,end) in self.edges})

    def edges_from(self, reversed = False):
        edges_from = {}
        for (start, end) in self.edges:
            if reversed: # we want the reverse graph, so just switch edges
                start, end = end, start
            if start not in edges_from:
                edges_from[start] = []
            if end not in edges_from:
                edges_from[end] = []
            edges_from[start].append(end)

        return edges_from

def first_pass(graph: Graph):
    for node in graph.reversed_edges_dict.keys():
        if not graph.explored[node]:
           graph = first_pass_dfs(graph, node)
    return graph

def first_pass_dfs(graph:Graph, node):
    graph.explored[node] = True
    for end_point in graph.reversed_edges_dict[node]:
        if not graph.explored[end_point]:
            graph.explored[end_point] = True
            first_pass_dfs(graph, end_point)
    graph.nodes_finished +=1
    graph.finishing_time[graph.nodes_finished-1]= node
    return graph


def second_pass(graph: Graph):
    for node in graph.finishing_time[::-1]:
        if not graph.explored[node]:
           nodes_explored =[node]
           graph, nodes_explored = second_pass_dfs(graph, node, nodes_explored)
           graph.sccs.append(nodes_explored)
    return graph

def second_pass_dfs(graph:Graph, node, nodes_explored):
    
    graph.explored[node] = True
    for end_point in graph.edges_dict[node]:
        if not graph.explored[end_point]:
            graph.explored[end_point] = True
            nodes_explored.append(end_point)
            second_pass_dfs(graph, end_point, nodes_explored)
    return graph, nodes_explored


def biggest_sccs(graph: Graph, top_sizes=5):
    scc_lengths = list(map(lambda x: len(x), graph.sccs))
    return sorted(scc_lengths)[-top_sizes:]


def main():
    sys.setrecursionlimit(2 ** 20)
    edges = process_input()
    #edges = [(1,2),(2,3),(3,3),(3,1),(3,5),(5,1)]
    graph = Graph(edges)
    graph = first_pass(graph)
    graph.reset_explored()
    graph = second_pass(graph)
    top_5_scc = biggest_sccs(graph)
    print(graph.finishing_time)
    print(graph.sccs)
    print(top_5_scc)


if __name__=="__main__":
    main()