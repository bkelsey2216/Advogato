import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv

G = nx.read_dot('advogato-graph-latest.dot')

# G = nx.DiGraph()
# G.add_edge('a', 'b')
# G.add_edge('a', 'a')
# G.add_edge('e', 'e')
# G.add_edge('b', 'c')

nodeList = G.nodes()
for node in nodeList:
	if G.has_edge(node, node):
		G.remove_edge(node, node)
		neighborsList = G.neighbors(node)
		if len(neighborsList) == 0:
			G.remove_node(node)

pos=nx.spring_layout(G)
nx.draw(G)
plt.show()


from networkx import *
import matplotlib.pyplot as plt
import pygraphviz as pgv

G = pgv.AGraph()

G.add_node('a')
G.add_edge('a', 'b')
G.add_edge('a', 'a')
G.add_edge('e', 'e')
G.add_edge('b', 'c')
G.layout()
G.draw('outTest.png')

G.write('fileOutTest.dot')

newG = pgv.AGraph('fileOutTest.dot')
newG.node_attr.update(color='red')

newG.layout('neato')
newG.draw('hasLoops.png')

nodeIter = newG.iternodes()
for item in nodeIter:
	if newG.has_edge(item, item):
		# remove loop
		newG.remove_edge(item, item)

		#get neighbors of looped node
		neighborsList = newG.neighbors(item)
		#if node has no neighbors, remove it
		if len(neighborsList) == 0:
			newG.remove_node(item)

newG.layout('neato')
newG.draw('noLoops.png')

networkXGraph = nx.from_pydot(newG)
nx.draw(networkXGraph)
plt.show()



# dataGraph = pgv.AGraph('advogato-graph-latest.dot')
# loopIter = dataGraph.iternodes()


# for node in loopIter:
# 	if dataGraph.has_edge(node, node):
#  		dataGraph.remove_edge(node, node)

#  		nList = dataGraph.neighbors(node)
#  		if len(nList) == 0:
#  			dataGraph.remove_node(node)

# dataGraph.layout()
# dataGraph.draw('noLoopDataset.png')
