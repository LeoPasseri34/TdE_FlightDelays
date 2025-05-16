import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapAirports = {}
        self._airports = DAO.getAllAirports()
        for a in self._airports:
            self._idMapAirports[a.ID] = a


    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self.addAllArchiV1()
        #print("Modo 1: N nodi: ", len(self._graph.nodes), "N archi: ", self._graph.number_of_edges())
        #self.addAllArchiv2()
        #print("Modo 2: N nodi: ", len(self._graph.nodes), "N archi: ", self._graph.number_of_edges())

    def addAllArchiV1(self):
        allEdges = DAO.getAllEdges(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                if self._graph.has_edge(e.aeroportoP, e.aeroportoD):
                    self._graph[e.aeroportoP][e.aeroportoD]["weight"] += e.peso
                else:
                    self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)



    def addAllArchiv2(self):
        allEdges = DAO.getAllEdgesV2(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)




    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes

    def getSortedNeighbours(self, nodo):
        neighbours = self._graph.neighbors(nodo)
        neighbTuples = []
        for n in neighbours:
            neighbTuples.append((n, self._graph[nodo][n]["weight"]))
        neighbTuples.sort(key=lambda x: x[1], reverse=True)
        return neighbTuples


    def getPath(self, v0, v1):
        path = nx.dijkstra_path(self._graph, v0, v1, weight=None)
        return path