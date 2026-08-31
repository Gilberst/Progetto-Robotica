import math
import sys
sys.path.append("../../")
from lib.ComunicationSystem.dds_sys import *
from movement.drone import *
from path_planner.position_calculator import * 
class Graph():
    def __init__(self):

        self.calculator=position_calculator()
        self.unweighted_graph = {
            0:[8,4,6,1,5,2,3,10],
            1:[5,13,6,0],
            2:[0,10,9,18,5],
            3:[0,8,16,10,15],
            4:[0,6,11,19,7,8],
            5:[0,2,18,12,13,1],
            6:[0,4,11,14,13,1],
            7:[4,8,15,19],
            8:[0,3,7,4],
            9:[17,10,2,18],
            10:[0,2,9,17,16,3],
            11:[19,4,6,14,20],
            12:[18,5,13],
            13:[12,5,1,6,14],
            14:[13,6,11,20],
            15:[3,7,19],
            16:[17,10,3],        
            17:[16,10,9],
            18:[9,2,5,12], 
            19:[15,7,4,11],
            20:[11,14],
        }
        self._graph:dict[int, list[tuple[int, float]]] = {}
        self._init_graph()

    def _init_graph(self):

        for key,nodes in self.unweighted_graph.items():
            self._graph[key]=[]
            
            for nodo in nodes:
                weight=self.calculator.euclidean_distance(key,nodo)
                self._graph[key].append((nodo,weight))

    def get_adiacents(self,node):
        return self._graph[node]
    
    def has_key(self,value):
        if value >=0 and value <=20:
            return True
        return False


class planner():
    def __init__(self) -> None:
        self._Graph=Graph()
        self.grafo=self._Graph._graph
        self.grafo_unw=self._Graph.unweighted_graph
    def Shortest_path(self,initial_pos, target):
        distance={nodo:float(math.inf)for nodo in self.grafo}
        distance[initial_pos]=0
        prev:dict[int,int|None]={nodo:None for nodo in self.grafo}

        _to_visit=set(self.grafo.keys())
        while _to_visit:
            current_min=min(_to_visit, key=lambda _node:distance[_node] )

            if distance[current_min]==math.inf:
                break

            if current_min==target:
                break

            _to_visit.remove(current_min)
            for adj, weight in self.grafo[current_min]:

                dist=distance[current_min]+weight

                if dist<=distance[adj]:
                    distance[adj]=dist
                    prev[adj]=current_min

        path_target=[]
        current_min=target

        while current_min is not None:
            path_target.append(current_min)
            current_min=prev[current_min]

        return_path=path_target.copy()
        path_target.reverse()

        if path_target[0]!=initial_pos:
            return None,None
        
        return path_target,return_path