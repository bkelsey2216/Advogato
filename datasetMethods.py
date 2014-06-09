## advogato graph attempt 1

import networkx as nx
import matplotlib.pyplot as plt

DG = nx.DiGraph()
masterDG = nx.DiGraph()
journeyerDG = nx.DiGraph()
apprenticeDG = nx.DiGraph()
subGraph = []
subDG = nx.DiGraph()
subMasterDG = nx.DiGraph()
subJourneyerDG = nx.DiGraph()
subApprenticeDG = nx.DiGraph()



def readFile():
	names = open('advogato/ent.advogato.user.name', 'r')
	edges = open('advogato/out.advogato', 'r')

	namesList = []
	lineArray = []

	for line in names:
		namesList.append(line)

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


def createSubgraphs():
	global subDG
	global subMasterDG
	global subJourneyerDG
	global subApprenticeDG 
	subDG = DG.subgraph(subGraph)
	subMasterDG = masterDG.subgraph(subGraph)
	subJourneyerDG = journeyerDG.subgraph(subGraph)
	subApprenticeDG = apprenticeDG.subgraph(subGraph)

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


def findAllPathsAtoB():
	pathList = []
	testPath = nx.DiGraph()

	for item in nx.all_simple_paths(subDG, subGraph[9], subGraph[17]):
		pathList.append(item)
		print item

	for x in pathList:
		iterator = len(x)

		for y in range(1, iterator):
			testPath.add_edge(x[y-1], x[y])
			 # for i in edge2DList:
			 # 	if x[y-1] == edge2DList[i][0]:
			 # 		if x[y] == edge2DList[i][1]:
				# 		testPath.add_weighted_edges_from([(x[y-1], x[y], edge2DList[i][2])])
								
	plt.figure(figsize=(10,10))
	pos=nx.spring_layout(testPath)
	nx.draw_networkx_nodes(testPath, pos, node_size = 75)
	nx.draw_networkx_labels(testPath, pos)
	nx.draw_networkx_edges(testPath, pos)
	# nx.draw_networkx_edges(testMasterDG, pos)
	# nx.draw_networkx_edges(testJourneyerDG, pos, edge_color = 'g')
	# nx.draw_networkx_edges(testApprenticeDG, pos, edge_color = 'b')
	plt.show()

def makeDistribution(numHops):
	statsArray = []
	for i in range (0,len(DG.nodes())):
		statsArray.append(0)

	done = False
	for node in DG.nodes():
		listOfReachables = []
		getListOfNodesReachableInNHops(numHops, 0, listOfReachables, node)
		numberOfNodesReachable = len(listOfReachables)
		if numberOfNodesReachable == 18 and  numHops == 1:
			print node
			#done = True

		statsArray[numberOfNodesReachable] += 1

	print statsArray[0:50]

def printReachableInNHops(numHops):

	listOfReachables = []
	node = subDG.nodes()[16]
	listOfReachables.append(node)
	print "the start node is %s" %node

	#getReachableInNHops(numberOfHops, depth, listOfReachables, node)
	getListOfNodesReachableInNHops(numHops, 0, listOfReachables, node)

	reachableWithin3HopsGraph  = subDG.subgraph(listOfReachables)

	print "The nodes reachable within %d hops of %s" %(numHops, node)
	print listOfReachables
	print "The length of the list is %d" %len(listOfReachables)
	nx.draw(reachableWithin3HopsGraph, with_labels = True)	
	plt.show()

#This method performs a recursive depth first search to add all the nodes within a 
#specified distance of the specified node

#returns a list containing all the nodes within numberOfHops 
def getListOfNodesReachableInNHops(numberOfHops, currentDepth, listOfReachables, node):
	if currentDepth == numberOfHops:
		return listOfReachables
	
	for n in DG.neighbors(node):
		if not n in listOfReachables:
			#print "appending %s" % n
			listOfReachables.append(n)
			getListOfNodesReachableInNHops(numberOfHops, currentDepth+1, listOfReachables, n)


readFile()
createSubgraphs()
makeDistribution(1)
makeDistribution(2)
makeDistribution(3)






