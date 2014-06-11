import pygraphviz
import networkx as nx
import matplotlib.pyplot as plt
import string

#This code removes numerical values from the .dot file because 
#the networkx read_dot method does not play well with numerical values
def removeNumbers():
	f = open('advogato-graph-latest.dot', 'r')
	o = open('temp-fixed-numbers.dot', 'w')

	for line in f:
		line = string.replace(line, "0","zero")
		line = string.replace(line, "1","one")
		line = string.replace(line, "2","two")
		line = string.replace(line, "3","three")
		line = string.replace(line, "4","four")
		line = string.replace(line, "5","five")
		line = string.replace(line, "6","six")
		line = string.replace(line, "7","seven")
		line = string.replace(line, "8","eight")
		line = string.replace(line, "9","nine")
		o.write(line)


G = nx.read_dot('exampleDotFile.dot')

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
	nx.write_dot(G, 'testOutputDot.dot')

DG = nx.DiGraph()
masterDG = nx.DiGraph()
journeyerDG = nx.DiGraph()
apprenticeDG = nx.DiGraph()
observerDG = nx.DiGraph()






# uncomment if you want to use it, or just ignore it: (SUPER SLOW)
# pos=nx.spring_layout(G)
# nx.draw(G)
# plt.show()
#removeNumbers()
#G = nx.read_dot('new.dot')
#makeCleanDOT()
removeKeys()

