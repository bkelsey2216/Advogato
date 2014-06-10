## advogato graph attempt 1

import pygraphviz
import networkx as nx
import matplotlib.pyplot as plt

# global variables
DG = nx.DiGraph()
masterDG = nx.DiGraph()
journeyerDG = nx.DiGraph()
apprenticeDG = nx.DiGraph()
subGraph = []
subDG = nx.DiGraph()
subMasterDG = nx.DiGraph()
subJourneyerDG = nx.DiGraph()
subApprenticeDG = nx.DiGraph()


# opens the username and edgelist files from the advogato dataset
# to read in and store graph data
def readFile():
	names = open('advogato/ent.advogato.user.name', 'r')
	edges = open('advogato/out.advogato', 'r')

	namesList = []
	lineArray = []

	for line in names:
		namesList.append(line.strip())

	for i in range(0,30):
		global subGraph
		subGraph.append(namesList[i-1])

	#declare 2D array and a counter variable, for storing 
	#source node, dest node, and their weights
	edge2DList = []
	count = 0
	for line in edges:
		edge2DList.append([])
		lineArray = line.split(' ', 3)

		sourceNode = namesList[int(lineArray[0]) - 1]
		destNode = namesList[int(lineArray[1]) - 1]
		rank = float(lineArray[2])
		global DG
		DG.add_weighted_edges_from([(sourceNode, destNode, rank)])

		# create a 2D array of all edges and weights
		for i in xrange(3):
			edge2DList[count].append(sourceNode)
			edge2DList[count].append(destNode)
			edge2DList[count].append(rank)
		count = count + 1

		if rank == 1:
			global masterDG
			masterDG.add_weighted_edges_from([(sourceNode, destNode, rank)])
		elif rank == .8:
			global journeyerDG
			journeyerDG.add_weighted_edges_from([(sourceNode, destNode, rank)])
		elif rank == .6:
			global apprenticeDG
			apprenticeDG.add_weighted_edges_from([(sourceNode, destNode, rank)])

	names.close()
	edges.close()

# create subgraphs based on certification, using lists of edges distingushed by
# weight and NetworkX's subgraph function
def createSubgraphs():
	global subDG
	global subMasterDG
	global subJourneyerDG
	global subApprenticeDG 
	subDG = DG.subgraph(subGraph)
	subMasterDG = masterDG.subgraph(subGraph)
	subJourneyerDG = journeyerDG.subgraph(subGraph)
	subApprenticeDG = apprenticeDG.subgraph(subGraph)

# Draws the subGraph of the whole dataset using different colors to specify
# certification levels on the directed edges (black = master, green = journeyman,
# blue = apprentice). Any nodes appearing unconnected on this graph is due to
# the fact that the subGraph only contains the first 50(ish) edges in the dataset.
def drawSubgraphs():
	plt.figure(figsize=(10,10))
	pos=nx.spring_layout(subDG)
	nx.draw_networkx_nodes(subDG, pos, node_size = 75)
	nx.draw_networkx_labels(subDG, pos)
	nx.draw_networkx_edges(subMasterDG, pos)
	nx.draw_networkx_edges(subJourneyerDG, pos, edge_color = 'g')
	nx.draw_networkx_edges(subApprenticeDG, pos, edge_color = 'b')
	nx.draw_networkx_labels(subDG, pos)
	plt.show()


#This function draws a graph of all paths from the source node and the destination node
#found in the dataset. Parameters 'source' and 'destination' refer to node numbers in the
#subGraph[] list of nodes.
#Example usage:
#	findAllPathsAtoB(9, 17) will find all paths from the 9th name in the username file
# 	to the 17th node in the username file. At present, these names are 'sh' and 'MikeCamel',
#	respectively.
def findAllPathsAtoB(source, destination):
	pathList = []
	testPath = nx.DiGraph()

	for item in nx.all_simple_paths(subDG, subGraph[source], subGraph[destination]):
		pathList.append(item)
		print item

	for x in pathList:
		iterator = len(x)

		for y in range(1, iterator):
			testPath.add_edge(x[y-1], x[y])

			#code segment attempting to identify the weights of the edges. 
			#currently it does not work.
			 # for i in edge2DList:
			 # 	if x[y-1] == edge2DList[i][0]:
			 # 		if x[y] == edge2DList[i][1]:
				# 		testPath.add_weighted_edges_from([(x[y-1], x[y], edge2DList[i][2])])
								
	plt.figure(figsize=(10,10))
	pos=nx.spring_layout(testPath)
	nx.draw_networkx_nodes(testPath, pos, node_size = 75)
	nx.draw_networkx_labels(testPath, pos)
	nx.draw_networkx_edges(testPath, pos)
	plt.show()

	# code to draw overlaying subgraphs based on weight. excluded because
	# currently cannot calculate weight of each edge.
	# nx.draw_networkx_edges(testMasterDG, pos)
	# nx.draw_networkx_edges(testJourneyerDG, pos, edge_color = 'g')
	# nx.draw_networkx_edges(testApprenticeDG, pos, edge_color = 'b')


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

	print statsArray[0:50]
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

readFile()
createSubgraphs()
#distWrite(makeDistribution(1), "distribution1.txt")
#distWrite(makeDistribution(2), "distribution2.txt")
#distWrite(makeDistribution(3), "distribution3.txt")
#distWrite(makeDistribution(4), "distribution4.txt")

#testReachableInNHops(2, DG.nodes()[59])

print nx.get_edge_attributes(DG,'weight')[0]






