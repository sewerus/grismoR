from multiprocessing import Value
import time
from simple_graph import SimpleGraph

def add_extended_permutations(bijection_list, queue, n):
    unused_vertices = list(range(n))
    for used_vertex in bijection_list:
        unused_vertices.remove(used_vertex)
    for vertex in unused_vertices:
        queue.put(bijection_list + [vertex])

def check_if_finish(id, bijection_list, n, finish_flag):
    if len(bijection_list) == n:
        finish_flag.set()
        # print("Worker %s - FOUND - %s" % (id, bijection_list))
        return True
    else:
        return False

def queue_worker_function(id, isomorfism_test, permutations_to_check, finish_flag, to_check_counter):
    n = isomorfism_test.n
    while not finish_flag.is_set():
        try:
            bijection_list = permutations_to_check.get_nowait()
        except:
            if to_check_counter.value == 0:
                break
            continue

        # print("Worker %s - start - %s - %s/%s" % (id, bijection_list, checked_counter.value, to_check_counter.value))
        if SimpleGraph(isomorfism_test.graph_2.subgraph_by_bijection(bijection_list)).matrix_compare_to_another(
                    SimpleGraph(isomorfism_test.graph_1.subgraph_by_bijection(range(len(bijection_list))))):
            check_if_finish(id, bijection_list, n, finish_flag)
            with to_check_counter.get_lock():
                to_check_counter.value += n - len(bijection_list)
            add_extended_permutations(bijection_list, permutations_to_check, n)
        with to_check_counter.get_lock():
            to_check_counter.value -= 1
        # print("Worker %s - end - %s/%s" % (id, checked_counter.value, to_check_counter.value))
