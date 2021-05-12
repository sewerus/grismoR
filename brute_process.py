from multiprocessing import Value
import time
from simple_graph import SimpleGraph

def pararell_brute_try_fix(isomorfism_test, bijection_list, finish_flag):
    # print("%s # %s" % (bijection_list[0], bijection_list))
    if finish_flag.is_set():
        # print("%s # %s # FINISHED" % (bijection_list[0], bijection_list))
        # return True without calculations because another thread confimed isomorphism
        return True
    else:
        if len(bijection_list) == isomorfism_test.n:
            if SimpleGraph(isomorfism_test.graph_2.subgraph_by_bijection(bijection_list)).matrix_compare_to_another(
                isomorfism_test.graph_1):
                # print("%s # %s # FINISHED FIRST #############################" % (bijection_list[0], bijection_list))
                finish_flag.set()
                return True
            else:
                return False
        elif not (SimpleGraph(isomorfism_test.graph_2.subgraph_by_bijection(bijection_list)).matrix_compare_to_another(
                    SimpleGraph(isomorfism_test.graph_1.subgraph_by_bijection(range(len(bijection_list)))))):
                return False
        else:
            unused_vertices = list(range(isomorfism_test.n))
            for used_vertex in bijection_list:
                unused_vertices.remove(used_vertex)
            for vertex in unused_vertices:
                if pararell_brute_try_fix(isomorfism_test, bijection_list + [vertex], finish_flag):
                    return True
            return False
