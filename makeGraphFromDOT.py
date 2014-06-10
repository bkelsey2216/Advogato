import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv


G = nx.read_dot('advogato-graph-latest.dot')

##This function creates a graph of the latest advogato dataset
##and outputs a new .dot file with the loops and unconnected nodes
##removed from the original .dot file
def makeCleanDOT():
	global G
	nodeList = G.nodes()
	for node in nodeList:
		if G.has_edge(node, node):
			G.remove_edge(node, node)
			neighborsList = G.neighbors(node)
			if len(neighborsList) == 0:
				G.remove_node(node)
	nx.write_dot(G, 'CLEAN-advogato-graph-latest.dot')

# uncomment if you want to use it, or just ignore it: (SUPER SLOW)
# pos=nx.spring_layout(G)
# nx.draw(G)
# plt.show()