import time
import bisect
# import threading
# from brute_thread import BruteThread, BruteThreadFinish
from multiprocessing import Process, Value, Queue, Pipe, Event
# from brute_process import BruteProcess
from brute_process import pararell_brute_try_fix
from queue_process import queue_worker_function
from simple_graph import SimpleGraph

class IsomorfismTest:
    def __init__(self, matrix_1, matrix_2, method, wl_dim=None):
        self.graph_1 = SimpleGraph(matrix_1)
        self.graph_2 = SimpleGraph(matrix_2)
        self.n = len(matrix_1)
        self.method = method
        self.time = 0
        self.result = False
        self.wl_dim = wl_dim

    def make_test(self):
        time_start = time.time()

        if self.method == "Brute":
            self.result = self.brute_method()
        elif self.method == "ParallelBrute":
            self.result = self.parallel_brute_method()
        elif self.method == "QueueBrute":
            self.result = self.queue_brute_method()
        elif self.method == "WL":
            self.result = self.wl_method()

        self.time = time.time() - time_start + 0.000000000001

    def queue_brute_method(self):
        workers_amount = self.n

        confirmed_isomorphism = Event()
        permutations_to_check = Queue()
        to_check_counter = Value('i', self.n)
        worker_processess = []

        #add single permutations to initiall Queue
        for v in range(self.n):
            permutations_to_check.put([v])

        #create and start processess
        for w in list(range(workers_amount)):
            worker = Process(target=queue_worker_function, args=(w, self, permutations_to_check, confirmed_isomorphism, to_check_counter))
            worker.start()
            worker_processess.append(worker)
            # print("Started worker: %d" % (w))

        for worker in worker_processess:
            worker.join()

        return bool(confirmed_isomorphism.is_set())

    # uses BruteProcess
    def parallel_brute_method(self):
        confirmed_isomorphism = Event()
        processess = []

        # create and start processess
        for v in list(range(self.n)):
            process = Process(target=pararell_brute_try_fix, args=(self, [v], confirmed_isomorphism))
            process.start()
            # print("Started process: %s" % (v))
            processess.append(process)

        # wait untill all processess are completed
        for process in processess:
            process.join()

        return bool(confirmed_isomorphism.is_set())

    def brute_method(self):
        return self.brute_try_fix([])

    def brute_try_fix(self, bijection_list):
        if not (SimpleGraph(self.graph_2.subgraph_by_bijection(bijection_list)).matrix_compare_to_another(
                SimpleGraph(self.graph_1.subgraph_by_bijection(range(len(bijection_list)))))):
            return False

        if len(bijection_list) == self.n:
            return SimpleGraph(self.graph_2.subgraph_by_bijection(bijection_list)).matrix_compare_to_another(
                self.graph_1)
        else:
            unused_vertices = list(range(self.n))
            for used_vertex in bijection_list:
                unused_vertices.remove(used_vertex)
            for vertex in unused_vertices:
                if self.brute_try_fix(bijection_list + [vertex]):
                    return True
            return False

    def wl_method(self):
        graph_1_neighbour_list = self.graph_1.neighbour_list()
        graph_2_neighbour_list = self.graph_2.neighbour_list()

        # vertices' colors
        graph_1_colors = [0] * self.n
        graph_2_colors = [0] * self.n

        # repeat method method_dim times
        for i in range(self.wl_dim):
            # calc collections of neighbours' colors for each vertex
            graph_1_collection = []
            graph_2_collection = []
            for vertex in range(self.n):
                neighbours_colors = []
                for neighbour in graph_1_neighbour_list[vertex]:
                    bisect.insort(neighbours_colors, graph_1_colors[neighbour])
                graph_1_collection.append(neighbours_colors)
                neighbours_colors = []
                for neighbour in graph_2_neighbour_list[vertex]:
                    bisect.insort(neighbours_colors, graph_2_colors[neighbour])
                graph_2_collection.append(neighbours_colors)

            # prepare color - collection pairs
            pairs = []
            color_index = 0
            for vertex in range(self.n):
                collection = graph_1_collection[vertex]
                if not collection in [row[1] for row in pairs]:
                    pairs.append([color_index, collection])
                    color_index += 1

            # check if all collections from graph_2 are in prepared pairs
            for vertex in range(self.n):
                if not graph_2_collection[vertex] in [row[1] for row in pairs]:
                    return False

            # assign new colors
            for vertex in range(self.n):
                graph_1_colors[vertex] = pairs[[row[1] for row in pairs].index(graph_1_collection[vertex])][0]
                graph_2_colors[vertex] = pairs[[row[1] for row in pairs].index(graph_2_collection[vertex])][0]

        # on the end compare vertices' colors
        for vertex in range(self.n):
            if graph_1_colors[vertex] != graph_1_colors[vertex]:
                return False

        # not returned False before
        return True
