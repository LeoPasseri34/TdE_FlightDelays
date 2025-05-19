import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapAirports = {}
        self._airports = DAO.getAllAirports()
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._bestPath = []
        self._bestObjFunction = 0


    def getCamminoOttimo(self, v0, v1, t):
        self._bestPath = []
        self._bestObjFunction = 0

        parziale = [v0]

        self._ricorsione(parziale, v1, t)
        return self._bestPath, self._bestObjFunction

    def _ricorsione(self, parziale, v1, t):
        # verificare se parziale è una possibile soluzione
            # verificare se parziale è meglio del best corrente
            # esco
        if parziale[-1] == v1:
            if self.getObjFunction(parziale) > self._bestObjFunction:
                self._bestObjFunction = self.getObjFunction(parziale)
                self._bestPath = copy.deepcopy(parziale)
        if len(parziale) == t+1:
            return

        # posso ancora aggiungere nodi
        # prendo i vicini e aggiungo un nodo alla volta
        # ricorsione
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()



    def getObjFunction(self, listOfNodes):
        val = 0
        for n in range(0, len(listOfNodes)-1):
            val += self._graph[listOfNodes[n]][listOfNodes[n+1]]["weight"]
        return val



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