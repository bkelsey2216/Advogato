## Natalie Pollard & Brooke Kelsey

import networkx as nx
import pygraphviz
import matplotlib.pyplot as plt

# global variables
DG = nx.DiGraph()
masterDG = nx.DiGraph()
journeyerDG = nx.DiGraph()
apprenticeDG = nx.DiGraph()
observerDG = nx.DiGraph()
listOfNodesForSubgraph = []
subDG = nx.DiGraph()
subMasterDG = nx.DiGraph()
subJourneyerDG = nx.DiGraph()
subApprenticeDG = nx.DiGraph()
subObserverDG = nx.DiGraph()
numberOfNodesToPlot = 200

##This method reads a "clean" (no self loops or nodes which point to nothing) .dot file
##from 'CLEAN-advogato-graph-latest.dot'
##When finished
##DG = a DiGraph of all the edges
##masterDG = a DiGraph of all of the edges ranked master
##journeyerDG, apprenticeDG, observerDG = similar to masterDG
##listOfNodesForSubgraph = a list of the first numberOfNodesToPlot nodes in the graph
##	this is used to create graphs of suitable size for viewing
##subDG = a graph of the nodes in listOfNodesForSubgraph for display purposes
##subMasterDG = a graph containing the master edges between nodes in listOfNodesForSubgraph
##subJourneyerDG, subApprenticeDG, subObserverDG = similar to subMasterDG
def readCleanDotFile():
	global DG
	global masterDG
	global journeyerDG
	global apprenticeDG
	global observerDG
	global numberOfNodesToPlot
	global listOfNodesForSubgraph
	global subDG
	global subMasterDG
	global subJourneyerDG
	global subApprenticeDG
	global subObserverDG
	
	DG = nx.DiGraph(nx.read_dot('CLEAN-advogato-graph-latest.dot'))
	levels = nx.get_edge_attributes(DG,'level')

	#sorts the edges into different graphs based on their levels for display purposes
	for i in DG.edges():
		if levels[(i[0], i[1])] == "Master":
			masterDG.add_edge(i[0],i[1])
		elif levels[(i[0], i[1])] == "Journeyer":
			journeyerDG.add_edge(i[0],i[1])
		elif levels[(i[0], i[1])] == "Apprentice":
			apprenticeDG.add_edge(i[0],i[1])
		elif levels[(i[0], i[1])] == "Observer":
			observerDG.add_edge(i[0],i[1])
		else:
			print "problem reading file"

	#creates smaller subgraphs for display purposes
	listOfNodesForSubgraph = DG.nodes()[0:numberOfNodesToPlot]
	subDG = DG.subgraph(listOfNodesForSubgraph)
	subMasterDG = masterDG.subgraph(listOfNodesForSubgraph)
	subJourneyerDG = journeyerDG.subgraph(listOfNodesForSubgraph)
	subApprenticeDG = apprenticeDG.subgraph(listOfNodesForSubgraph)
	subObserverDG = observerDG.subgraph(listOfNodesForSubgraph)


# Draws the listOfNodesForSubgraph of the whole dataset using different colors to specify
# certification levels on the directed edges (black = master, green = journeyman,
# blue = apprentice, yellow = observer). Any nodes appearing unconnected on this graph is due to
# the fact that the listOfNodesForSubgraph only contains the first numberOfNodesToPlot nodes in the dataset.
# ie. they are connected to nodes which are not being displayed
def drawSubgraphs():
	plt.figure(figsize=(10,10))
	pos=nx.spring_layout(subDG)
	nx.draw_networkx_nodes(subDG, pos, node_size = 75)
	nx.draw_networkx_labels(subDG, pos)
	nx.draw_networkx_edges(subMasterDG, pos)
	nx.draw_networkx_edges(subJourneyerDG, pos, edge_color = 'g')
	nx.draw_networkx_edges(subApprenticeDG, pos, edge_color = 'b')
	nx.draw_networkx_edges(subObserverDG, pos, edge_color = 'y')
	plt.show()


#This function draws a graph of all paths from the source node and the destination node
#found in the dataset. Parameters 'source' and 'destination' refer to node numbers in the
#listOfNodesForSubgraph[] list of nodes.
#Example usage:
#	findAllPathsAtoB(9, 17) will find all paths from the 9th name in the username file
# 	to the 17th node in the username file. At present, these names are 'sh' and 'MikeCamel',
#	respectively.
def findAllPathsAtoB(source, destination):
	pathList = []
	testPath = nx.DiGraph()

	for item in nx.all_simple_paths(subDG, listOfNodesForSubgraph[source], listOfNodesForSubgraph[destination]):
		pathList.append(item)
		print item

	for x in pathList:
		iterator = len(x)

		for y in range(1, iterator):
			testPath.add_edge(x[y-1], x[y])
								
	plt.figure(figsize=(10,10))
	pos=nx.spring_layout(testPath)
	nx.draw_networkx_nodes(testPath, pos, node_size = 75)
	nx.draw_networkx_labels(testPath, pos)
	nx.draw_networkx_edges(testPath, pos)
	plt.show()


#This returns an array of integers of size number of nodes. The integer at 
#each position in the array represents the number of nodes which can reach this many
#other nodes
#For example statsArray[5] == 50 indicates that there are 50 nodes that can reach exactly 5 other nodes
def makeDistribution(numHops):
	statsArray = []
	for i in range (0,len(DG.nodes())):
		statsArray.append(0)

	for node in DG.nodes():
		listOfReachables = []
		getListOfNodesReachableInNHops(numHops, 0, listOfReachables, node)
		numberOfNodesReachable = len(listOfReachables)

		statsArray[numberOfNodesReachable] += 1

	##prints the first 50 items of stats array -- uncomment to check our algorithm output
	#print statsArray[0:50]
	return statsArray

#This method tests reachable in n hops by printing out all the nodes reachable
#within numHops of node and displaying a graph of these nodes
#Even if the user has not rated themselves they will still appear in the 
#displayed network
def testReachableInNHops(numHops, node):

	listOfReachables = []
	getListOfNodesReachableInNHops(numHops, 0, listOfReachables, node)

	print "The nodes reachable within %d hops of %s" %(numHops, node)
	print listOfReachables
	print "The number of nodes reachable is %d" %len(listOfReachables)

	#add node to list of reachables before making the subgraph to display
	#(because otherwise it looks funny)
	if not node in listOfReachables:
		listOfReachables.append(node)

	reachableGraph  = DG.subgraph(listOfReachables)

	nx.draw(reachableGraph, with_labels = True)	
	plt.show()

#This method performs a recursive depth first search to add all the nodes within a 
#specified distance of the specified node to the listOfReachables
#current depth should be set to zero
#listOfReachables should be an empty list
def getListOfNodesReachableInNHops(numberOfHops, currentDepth, listOfReachables, node):
	if currentDepth == numberOfHops:
		return listOfReachables
	
	for n in DG.neighbors(node):
		if not n in listOfReachables:
			listOfReachables.append(n)
			getListOfNodesReachableInNHops(numberOfHops, currentDepth+1, listOfReachables, n)

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

readCleanDotFile()

#calls DFS search to get 4 distribution data files
distWrite(makeDistribution(1), "distribution1.txt")
distWrite(makeDistribution(2), "distribution2.txt")
distWrite(makeDistribution(3), "distribution3.txt")
distWrite(makeDistribution(4), "distribution4.txt")

drawSubgraphs()






