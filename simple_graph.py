import numpy as np


class SimpleGraph:
    def __init__(self, matrix):
        self.all_dfs_branches = []
        self.matrix = []
        for row in matrix:
            self.matrix.append([])
            for x in row:
                self.matrix[-1].append(x)
        self.n = len(matrix)

    def matrix_compare_to_another(self, another_graph):
        if self.n == len(another_graph.matrix):
            end_test = False
            result = True
            # test only last added vertex
            i = self.n - 1
            for j in range(self.n):
                if self.matrix[i][j] != another_graph.matrix[i][j]:
                    result = False
                    end_test = True
                    break
        else:
            result = False
        return result

    def swap_vertices(self, a: int, b: int):
        old_a_neighbours = []
        old_b_neighbours = []
        for i in range(self.n):
            if self.matrix[i][a]:
                old_a_neighbours.append(i)
            if self.matrix[i][b]:
                old_b_neighbours.append(i)
        for i in range(self.n):
            self.matrix[i][a] = False
            self.matrix[a][i] = False
            self.matrix[i][b] = False
            self.matrix[b][i] = False
        for x in old_a_neighbours:
            if x == b:
                self.matrix[b][a] = True
                self.matrix[a][b] = True
            else:
                self.matrix[b][x] = True
                self.matrix[x][b] = True
        for x in old_b_neighbours:
            if x == a:
                self.matrix[a][b] = True
                self.matrix[b][a] = True
            else:
                self.matrix[a][x] = True
                self.matrix[x][a] = True

    def neighbour_list(self):
        result = []
        for i in range(self.n):
            result.append([])
        for i in range(self.n - 1):
            for j in range(i, self.n):
                if self.matrix[i][j]:
                    result[i].append(j)
                    result[j].append(i)
        return result

    def subgraph_by_bijection(self, bijection_list):
        new_matrix = []
        new_n = len(bijection_list)
        for i in range(new_n):
            new_matrix.append([])
            for j in range(new_n):
                new_matrix[-1].append(False)
        for i in range(new_n-1):
            for j in range(i, new_n):
                if self.matrix[bijection_list[i]][bijection_list[j]]:
                    new_matrix[i][j] = True
                    new_matrix[j][i] = True
        return new_matrix

    def is_consistent(self):
        neighbour_list = self.neighbour_list()
        start_vertex = 0
        # mark all the vertices as not visited
        visited = [False] * len(neighbour_list)
        # create a queue for BFS
        queue = []
        # mark the source node as visited and enqueue it
        queue.append(start_vertex)
        visited[start_vertex] = True
        while queue:
            # dequeue a vertex from queue and print it
            s = queue.pop(0)
            # get all adjacent vertices of the dequeued vertex s.
            # if a adjacent has not been visited, then mark it visited and enqueue it
            for i in neighbour_list[s]:
                if not(visited[i]):
                    queue.append(i)
                    visited[i] = True
        result = True
        for vertex_visited in visited:
            if not vertex_visited:
                result = False
                break
        return result
