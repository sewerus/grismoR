import threading
import time
# from isomorfism_test import IsomorfismTest
from simple_graph import SimpleGraph

class BruteThreadFinish:
    def __init__(self):
        self.value = False
    def set_finish(self):
        self.value = True
    def check(self):
        return self.value

class BruteThread (threading.Thread):
    def __init__(self, base_vertex, isomorfism_test, finish):
        threading.Thread.__init__(self)
        self.base_vertex = base_vertex
        self.isomorfism_test = isomorfism_test
        self.finish = finish

    def run(self):
        self.pararell_brute_try_fix([self.base_vertex])
        print("################## End of thread %s" % (self.base_vertex))

    def pararell_brute_try_fix(self, bijection_list):
        print("%s # %s" % (self.base_vertex, bijection_list))
        if self.finish.check():
            print("%s # %s # FINISHED" % (self.base_vertex, bijection_list))
            # return True without calculations because another thread confimed isomorphism
            return True
        else:
            if len(bijection_list) == self.isomorfism_test.n:
                if SimpleGraph(self.isomorfism_test.graph_2.subgraph_by_bijection(bijection_list)).matrix_compare_to_another(
                    self.isomorfism_test.graph_1):
                    print("%s # %s # FINISHED FIRST #############################" % (self.base_vertex, bijection_list))
                    self.finish.set_finish()
                    return True
                else:
                    return False
            elif not (SimpleGraph(self.isomorfism_test.graph_2.subgraph_by_bijection(bijection_list)).matrix_compare_to_another(
                        SimpleGraph(self.isomorfism_test.graph_1.subgraph_by_bijection(range(len(bijection_list)))))):
                    return False
            else:
                unused_vertices = list(range(self.isomorfism_test.n))
                for used_vertex in bijection_list:
                    unused_vertices.remove(used_vertex)
                for vertex in unused_vertices:
                    if self.pararell_brute_try_fix(bijection_list + [vertex]):
                        return True
                return False
