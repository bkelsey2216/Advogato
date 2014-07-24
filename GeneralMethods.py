## Natalie Pollard & Brooke Kelsey
import networkx as nx
import string
from TVSL3 import TVSLTran #transfer edge attributes to opinion
import csv
import random


## This method returns a networkx graph of the .dot file specified by filename
## It removes all the self loops and nodes with no edges
def readDotFile(fileName):
	DG = nx.DiGraph(nx.read_dot(fileName))

	#remove all of the self loop edges
	DG.remove_edges_from(DG.selfloop_edges())

	#remove all nodes with no edges
	toRemove = []
	for node in DG:
		if DG.in_degree(node) == 0 and DG.out_degree(node) == 0:
			toRemove.append(node)
	DG.remove_nodes_from(toRemove)

	return DG

## This method returns a dictionary with the nodes in graph as keys and 
## the number of the node in the graph as the value
def getNodeIntDict(graph):
	ints = nx.convert_node_labels_to_integers(graph,label_attribute='old_name')
	nodeIntList = ints.nodes()
	nodeIntDict = {}	
	for n in nodeIntList:
		nodeIntDict[(ints.node[n]['old_name'])] = n
	return nodeIntDict


##distWrite creates a file with the given filename and writes
##one element of the given array into one line of the file. These
##files will be used to create data vectors for a distribution.
## 	Parameters: 
##		distArray - an array
##		filename - a string containing the user-specified filename
def distWrite(distArray, filename):

	outFile = open(filename, 'w')
	x = len(distArray)
	for index in range(0, x):
		outFile.write(str(distArray[index]) + '\n')

	outFile.close()


# Helper method for writing 3 levels to a file
# Useful for testing cocitaion and coupling and propagation
def writeTriangleOfTrust(XLevel,YLevel,ZLevel,filename):
	XOpinion = TVSLTran(XLevel)
	YOpinion = TVSLTran(YLevel)
	ZOpinion = TVSLTran(ZLevel)

	with open(filename, 'a') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		toWrite.writerow([XOpinion[0], XOpinion[1], XOpinion[2], XOpinion[3], 
		YOpinion[0], YOpinion[1], YOpinion[2], YOpinion[3], ZOpinion[0], 
		ZOpinion[1], ZOpinion[2], ZOpinion[3]])

#This code removes numerical values from the .dot file because 
#the networkx read_dot method does not play well with numerical values
def removeNumbers(inFileName, outFileName):
	f = open(inFileName, 'r')
	o = open(outFileName, 'w')

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

# Returns the nodes of a triangle in the graph
# where A -> B, A -> C, B -> C
def findRandomTriangle(graph):
	while True:
		A = random.choice(graph.nodes())
		neighbors = graph.neighbors(A)
		if len(neighbors) >= 2:
			(B,C) = random.sample(neighbors,2)
			if graph.has_edge(B,C):
				return (A,B,C)

def getTrustorsOfExactHop(DG, node, numHops):
	reverseDG = DG.reverse()
	dictOfPathLengths = nx.single_source_shortest_path_length(reverseDG, node, cutoff = numHops)
	return [x for x in dictOfPathLengths.keys() if dictOfPathLengths[x] == numHops]

def getTrusteesOfExactHop(DG, node, numHops):
	dictOfPathLengths = nx.single_source_shortest_path_length(DG, node, cutoff = numHops)
	return [x for x in dictOfPathLengths.keys() if dictOfPathLengths[x] == numHops]

