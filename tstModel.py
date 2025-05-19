import networkx as nx

from model.model import Model

mymodel = Model()
mymodel.buildGraph(5)

v0 = mymodel.getAllNodes()[0]
connessa = list(nx.node_connected_component(mymodel._graph, v0))

v1 = connessa[10]

print(v0, v1)

bestPath, bestObjFun = mymodel.getCamminoOttimo(v0, v1, 4)
print("------------------------")
print(f"Il cammino ottimo tra {v0} e {v1} ha peso = {bestObjFun} \n {bestPath}")