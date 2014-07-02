## Natalie Pollard & Brooke Kelsey

import networkx as nx
import pygraphviz
import matplotlib.pyplot as plt
from collections import defaultdict
from decimal import Decimal
import csv
from TVSL3 import TVSLTran #transfer edge attributes to opinion
from TVSL3 import TVSLAlgr #trust assess algr
from TVSL3 import TVSLExp #compute expected belief
from TVSL3 import comb #combining operation

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
	
	DG = nx.DiGraph(nx.read_dot('advogato-fixed-numbers.dot'))

	
	#remove all of the self loop edges
	DG.remove_edges_from(DG.selfloop_edges())
	#remove all nodes with no incoming edges

	toRemove = []
	for node in DG:
		if DG.in_degree(node) == 0 and DG.out_degree(node) == 0:
			toRemove.append(node)
	DG.remove_nodes_from(toRemove)

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
def makeReachableDistribution(numHops):
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

def makeDegreeDistribution():
	statsArray = []
	for i in range (0,len(DG.nodes())):
		statsArray.append(0)

	for node in DG:		
		statsArray[DG.in_degree(node)] += 1

	##prints the first 50 items of stats array -- uncomment to check our algorithm output
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

#This method performs a recursive depth first search to add all the nodes which have edges
#pointing to a specicied node within a specified distance
#current depth should be set to zero
#listOfReachers should be an empty list
def getSourcesUsingDestInNHops(numberOfHops, currentDepth, listOfReachers, destination):
	if currentDepth == numberOfHops:
		return listOfReachers

	for n in DG.predecessors(destination):
		if not n in listOfReachers:
			listOfReachers.append(n)
			getSourcesUsingDestInNHops(numberOfHops, currentDepth+1, listOfReachers, n)


## creates and returns a dictionary of key=node:value=inDegree for all nodes in the graph
## having an inDegree *greater than or equal to* the inDegree parameter
def getNodesXInDegree(inDegree):
	nodeListDict = {}
	for node in DG:
		if DG.in_degree(node) >= inDegree:
			nodeListDict[node] = DG.in_degree(node)

	return nodeListDict

## creates and returns a dictionary of key=node:value=inDegree for all nodes in the graph
## having an inDegree *less than or equal to* the inDegree parameter
def getNodesYInDegree(inDegree):
	nodeListDict = {}
	for node in DG:
		if DG.in_degree(node) <= inDegree and DG.in_degree(node) > 0:
			nodeListDict[node] = DG.in_degree(node)

	return nodeListDict

# combine the opinions of the predecessors coming into the node
# and return the public opinion vector
def computePublicOpinion(node):
	predecessors = DG.predecessors(node)
	if len(predecessors) < 0:
		print "Error: cannot compute public opinion of a node with no predecessors"

	level = DG[predecessors[0]][node]['level']
	currentOpinion = TVSLTran(level)

	for i in range(1,len(predecessors)):
		level = DG[predecessors[i]][node]['level']
		toCombine = TVSLTran(level)
		currentOpinion = comb(toCombine, currentOpinion)

	return currentOpinion


# returns all nodes with shortest path exaclty numHops from node
def getTrustorsOfExactHop(node, numHops):
	trustorNodes = []
	getSourcesUsingDestInNHops(numHops, 0, trustorNodes, node)
	toRemove = []

	# If shortest path between the trustor and the node is not 
	# numHops then remove it from trustorNodes
	for trustor in trustorNodes:
		if nx.shortest_path_length(DG, trustor, node) != numHops:
			toRemove.append(trustor)	

	for removeNode in toRemove:
		trustorNodes.remove(removeNode)

	return trustorNodes

# This method calls compute public opinion on all the users
# in userDict. It then calculates the opinion of each node exacly
# numHops away. It outputs these opinions in the format 
# [groupID (1 = X, 2 = Y); trusteeID; inDegree of trustee; trustorID; trustor's opinion; public opinion]
# to the file groupID + "output.csv"
def calculateOpinionsAndWriteToFile(numHops, userDict, groupID):
	# This variable is the additional length witch can be added to numhops
	# (The one you suggested be 3 in your instructions)
	# Altering this variable will significantly impact runtime
	additionToPathLength = 1

	# Integers representing each node for file writing purposes
	DGInts = nx.convert_node_labels_to_integers(DG,label_attribute='old_name')  
	nodeIntList = DGInts.nodes()
	nodeIntDict = {}	
	for n in nodeIntList:
		nodeIntDict[(DGInts.node[n]['old_name'])] = n


	with open(str(groupID) + 'output.csv', 'wb') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		
		for node in userDict:
			print "For node " + node						

			# the public opinion is the comined opinion of all nodes 1 hop away
			publicOpinion = computePublicOpinion(node)
			print "The public opinion is " + str(publicOpinion)			
			
			# trustor nodes is the list of nodes with shortest path numHops to node
			trustorNodes = getTrustorsOfExactHop(node, numHops)

			for trustor in trustorNodes:
				pubOpnDG = nx.DiGraph()

				# fill pubOpnDG	with all the edges which occur in paths of length numHops + additionToPathLength
				# from trustor to node	
				path = nx.all_simple_paths(DG, source=trustor, target=node, cutoff=numHops + additionToPathLength)			
				for p in path:
					for i in range(0, len(p)-1):
						pubOpnDG.add_edge(p[i], p[i+1], level=DG[p[i]][p[i+1]]['level'])

				if trustor != node:
					currentOpinion = TVSLAlgr(pubOpnDG, trustor, node, numHops + additionToPathLength, 0)
					print trustor + "'s opinion of " + node + " is " + str(currentOpinion)
					# big file writing statement
					toWrite.writerow([groupID, nodeIntDict[node], userDict[node], 
					nodeIntDict[trustor], currentOpinion[0], currentOpinion[1], 
					currentOpinion[2], currentOpinion[3], publicOpinion[0], publicOpinion[1], 
					publicOpinion[2], publicOpinion[3]])

# Finds nodes 
# write the trust vectors to the file in the order 
# X (start->middle), Y (middle->dest), Z (start->dest)
# output file = TransitiveOutput.csv
def testTrustTransitivity():
	for dest in DG.nodes():
		for pred in DG.predecessors(dest):
			allPaths = nx.all_simple_paths(DG,pred,dest,2)
			for path in allPaths:
				if len(path) == 3:
					writeForTransitivity(path)


# helper method for testTrustTransitivity to calculate the 
# trust vectors and write the vectors to the file
def writeForTransitivity(path):
	XLevel = DG[path[0]][path[1]]['level']
	YLevel = DG[path[1]][path[2]]['level']
	ZLevel = DG[path[0]][path[2]]['level']

	XOpinion = TVSLTran(XLevel)
	YOpinion = TVSLTran(YLevel)
	ZOpinion = TVSLTran(ZLevel)

	with open('TransitiveOutput.csv', 'a') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		toWrite.writerow([XOpinion[0], XOpinion[1], XOpinion[2], XOpinion[3], 
		YOpinion[0], YOpinion[1], YOpinion[2], YOpinion[3], ZOpinion[0], 
		ZOpinion[1], ZOpinion[2], ZOpinion[3]])

# returns nodes start, dest, mid1 and mid2 where there is an edge start->dest and
# nodes mid1 and one mid2 such that there are edges start->mid1->dest and start->mid2->dest and
# mid1 != mid2
def testTrustCombining():
	for dest in DG.nodes():
		for pred in DG.predecessors(dest):
			allPaths = nx.all_simple_paths(DG,pred,dest,2)
			allPathsList = []
			for path in allPaths:
				if len(path) == 3:
					allPathsList.append(path)
			if len(allPathsList) >= 2:
				path1 = allPathsList[0]
				path2 = allPathsList[1]

				print "path1 " + str(path1)
				print "path2 " + str(path2)

				writeForCombining(path1,path2)


# write the trust vectors to the file in the order X (disc(start->mid1, mid1->dest)),
# Y (disc(start->mid2, mid2->dest)), Z (start->dest)
def writeForCombining(path1, path2):
# output file = combinedTransitiveOutput.csv
	
	XALevel = DG[path1[0]][path1[1]]['level']
	XBLevel = DG[path1[1]][path1[2]]['level']
	
	YALevel = DG[path2[0]][path2[1]]['level']
	YBLevel = DG[path2[1]][path2[2]]['level']

	ZLevel  = DG[path1[0]][path1[2]]['level']

	XAOpinion = TVSLTran(XALevel)
	XBOpinion = TVSLTran(XBLevel)
	YAOpinion = TVSLTran(YALevel)
	YBOpinion = TVSLTran(YBLevel)

	XOpinion = disc(XAOpinion, XBOpinion)
	YOpinion = disc(YAOpinion, YBOpinion)
	ZOpinion = TVSLTran(ZLevel)

	with open('combinedTransitiveOutput.csv', 'a') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		toWrite.writerow([XOpinion[0], XOpinion[1], XOpinion[2], XOpinion[3], 
		YOpinion[0], YOpinion[1], YOpinion[2], YOpinion[3], ZOpinion[0], 
		ZOpinion[1], ZOpinion[2], ZOpinion[3]])


#read in the file
readCleanDotFile()

getNodesWithCorrectTopologyForTransitivity()


#usersX = getNodesXInDegree(150)
#print "Calculating the public opinion for %d users" %len(usersX.keys())
#calculateOpinionsAndWriteToFile(2, usersX, 1)
#print
#usersY = getNodesYInDegree(20)
#print "Calculating the public opinion for %d users" %len(usersY.keys())
#calculateOpinionsAndWriteToFile(2, usersY, 2)






