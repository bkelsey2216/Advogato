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
from TVSL3 import disc
import random
import scipy as sp
import numpy as np

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
##from 'advogato-fixed-numbers.dot'
##When finished
##DG = a DiGraph of all the edges
def readCleanDotFile():
	global DG
	DG = nx.DiGraph(nx.read_dot('advogato-fixed-numbers.dot'))
	
	#remove all of the self loop edges
	DG.remove_edges_from(DG.selfloop_edges())
	#remove all nodes with no incoming edges

	toRemove = []
	for node in DG:
		if DG.in_degree(node) == 0 and DG.out_degree(node) == 0:
			toRemove.append(node)
	DG.remove_nodes_from(toRemove)

#make smaller graphs for each level in order to display and visualize
##masterDG = a DiGraph of all of the edges ranked master
##journeyerDG, apprenticeDG, observerDG = similar to masterDG
##listOfNodesForSubgraph = a list of the first numberOfNodesToPlot nodes in the graph
##	this is used to create graphs of suitable size for viewing
##subDG = a graph of the nodes in listOfNodesForSubgraph for display purposes
##subMasterDG = a graph containing the master edges between nodes in listOfNodesForSubgraph
##subJourneyerDG, subApprenticeDG, subObserverDG = similar to subMasterDG
def makeGraphForEachLevel():
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


# Finds all the nodes start and dest in the graph with the topology
# start -> dest and start -> mid1 -> dest and start->mid2->dest where mid1 != mid2
# Write the trust vectors to the output file 
# combinedTransitiveOutput.csv
# in the order: X (disc(start->mid1, mid1->dest)), Y (disc(start->mid2, mid2->dest)), Z (start->dest)
def testTrustCombining():
	#open the file and write nothing, clearing the file
	open('combinedTransitiveOutput.csv', 'w').close()
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

				writeForCombining(path1,path2)


# helper method for testTrustCombining to calculate the 
# trust vectors and write the vectors to the file
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


# This method tests CoCitation, Coupling and Transitivity as
# outlined in the Matiri paper.
# All of these require a topolpology with egdes node -> node2,
# node -> node3 and node2 -> node3
# The only difference between the outputs is which node is 
# considdered X, Y and Z
def testCocitationCouplingAndTransitivity():
	#open the files and write nothing, clearing the file
	open('CoCitation.csv', 'w').close()
	open('Coupling.csv', 'w').close()
	open('Propagation.csv', 'w').close()

	numberOfSets = 0
	while numberOfSets < 1000:
		rand = random.randint(0,len(DG.nodes())-1)
		node1 = DG.nodes()[rand]
		neighbors = DG.neighbors(node1)
		if len(neighbors) > 2:
			rand1 = random.randint(0,len(neighbors)-1)
			rand2 = random.randint(0,len(neighbors)-1)
			
			#make sure rand1 != rand2
			while rand1 == rand2:
				rand2 = random.randint(0,len(neighbors)-1)
			node2 = neighbors[rand1]
			node3 = neighbors[rand2]

			#if the correct topology is present
			#ie. there exist edges
			# node -> node2
			# node -> node3
			# node2 -> node3
			if DG.has_edge(node2,node3):
				numberOfSets +=1

				#co-citatoin
				XLevel = DG[node1][node2]['level']
				YLevel = DG[node1][node3]['level']
				ZLevel = DG[node2][node3]['level']
				writeTriangleOfTrust(XLevel,YLevel,ZLevel,"CoCitation.csv")
				#coupling
				XLevel = DG[node2][node3]['level']
				YLevel = DG[node1][node3]['level']
				ZLevel = DG[node1][node2]['level']
				#propogation(transitivity)
				writeTriangleOfTrust(XLevel,YLevel,ZLevel,"Coupling.csv")
				XLevel = DG[node1][node2]['level']
				YLevel = DG[node2][node3]['level']
				ZLevel = DG[node1][node3]['level']
				writeTriangleOfTrust(XLevel,YLevel,ZLevel,"Propagation.csv")							

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
	

# For every node in the first 1000 nodes this method checks the length of the
# shortest path to every other node in the graph. It creates a distribution
# where each entry represents the length of a shortest path and 0 indicates
# no path. It outputs this distribution to the file smallworld.txt.
def smallWorldProblem():
	distribution = []
	for i in range(0,50):
		distribution.append(0)

	for source in DG.nodes()[0:1000]:
		for dest in DG.nodes():
			if source != dest:
				if nx.has_path(DG,source,dest) == False:
					distribution[0] +=1
				else:
					distribution[nx.shortest_path_length(DG, source, dest)] +=1

	print distribution
	distWrite(distribution,"smallworld.txt")



# This method randomly finds 1000 pairs of nodes with shortest path numHops between 
# them. It calculates the trust between these nodes using 3VSL. It outputs the resulting 
# trust vector to str(numHops) + distance.csv
def doesNeutralityIncreaseWithDistance(numHops):
	numberOfPairs = 0
	additionToPathLength = 1

	with open(str(numHops) + 'distance.csv', 'wb') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		
		while numberOfPairs < 1000:
			rand = random.randint(0,len(DG.nodes())-1)
			node = DG.nodes()[rand]
			trustorNodes = getTrustorsOfExactHop(node, numHops)
			if len(trustorNodes) > 0:
				rand = random.randint(0,len(trustorNodes)-1)
				trustor = trustorNodes[rand]			
	
				# fill tvslDG with all the edges which occur in paths of length numHops + additionToPathLength
				# from trustor to node
				tvslDG = nx.DiGraph()	
				path = nx.all_simple_paths(DG, source=trustor, target=node, cutoff=numHops + additionToPathLength)			
				for p in path:
					for i in range(0, len(p)-1):
						tvslDG.add_edge(p[i], p[i+1], level=DG[p[i]][p[i+1]]['level'])
				
				currentOpinion = TVSLAlgr(svslDG, trustor, node, numHops + additionToPathLength, 0)
				print trustor + "'s opinion of " + node + " is " + str(currentOpinion)
				
				# big file writing statement
				toWrite.writerow([currentOpinion[0], currentOpinion[1], 
				currentOpinion[2], currentOpinion[3]])

				numberOfPairs += 1



# This function traverses all nodes in the graph to find pairs A,B such that A->B and B->A are
# both edges that exist in the dataset. Taking care to not repeat pairs, the function appends these
# pairs to a 'listofReciprocates'. It then forms a sample population of 1000 such reciprocative relationships
# using random.sample, and returns this sublist to the function caller.
def findReciprocatingTrust():
	listofReciprocates = []
	for node in DG.nodes():
		listofNeighbors = DG.neighbors(node)
		for neighbor in listofNeighbors:
			if DG.has_edge(neighbor, node):
				newPair = [node, neighbor]
				checknewPair = [neighbor, node]
				if (newPair not in listofReciprocates) and (checknewPair not in listofReciprocates):
					listofReciprocates.append(newPair)

	sampleRelationships = random.sample(listofReciprocates, 1000)

	return sampleRelationships

# This function takes the random sample of mutual trusting nodes, finds their respective opinions
# by indexing into the graph edge weights, transforms these edge weights into an opinion using TVSLTran,
# and writes these two opinions onto one line of a .csv file. This .csv file will be the input to
# MATLAB code computing the expected belief for a CDF.
def computeTrustDifference():
	#open the file and write nothing, clearing the file
	open('reciprocativeTrust.csv', 'w').close()
	relationships = findReciprocatingTrust()
	for pair in relationships:
		levelAB = DG[pair[0]][pair[1]]['level']
		levelBA = DG[pair[1]][pair[0]]['level']
		trustAB = TVSLTran(levelAB)
		trustBA = TVSLTran(levelBA)

		with open('reciprocativeTrust.csv', 'a') as csvfile:
			toWrite = csv.writer(csvfile, delimiter = ',')
			toWrite.writerow([trustAB[0], trustAB[1], trustAB[2], trustAB[3], trustBA[0], trustBA[1], trustBA[2]])

# This function selects random pairs of nodes and checks whether a path exists between them.
# If a path does exist, it computes the length of the shortest path and gets a list of nodes on
# the shortest path. The opinions along this path are then discounted into one final opinion
# connecting the original pair of nodes. The final opinion and path length are written into
# a line of a .csv file for Experiment 4 data analysis.
def makeOpinionFile():	
	pairsList = []
	#open and close file to make blank
	open('opinionsList.csv', 'w').close()

	# file format: [pairOpinion[0], pairOpinion[1], pairOpinion[2], pairOpinion[3], pathLength]

	#need a sample of 1000 opinions. hopefully running for 50000 iterations will produce a list
	# that has at least 1000 opinions with expected belief over 0.75
	for i in range(0, 100000):
		newPair = random.sample(DG.nodes(), 2)
		if newPair not in pairsList:
			print str(len(pairsList))
			if nx.has_path(DG, newPair[0], newPair[1]):
				pairsList.append(newPair)
				pathLength = nx.shortest_path_length(DG, newPair[0], newPair[1])
				path = nx.shortest_path(DG, newPair[0], newPair[1])
				cert = DG[path[0]][path[1]]['level']
				pairOpinion = TVSLTran(cert)

				print newPair
				print path
				for x in range(1, len(path)-1):
					nextCert = DG[path[x]][path[x+1]]['level']
					nextOpinion = TVSLTran(nextCert)
					pairOpinion = disc(pairOpinion, nextOpinion)

				with open('opinionsList.csv', 'a') as csvfile:
					toWrite = csv.writer(csvfile, delimiter = ',')
					toWrite.writerow([pathLength, pairOpinion[0], pairOpinion[1], pairOpinion[2], pairOpinion[3]])

readCleanDotFile()
testCocitationCouplingAndTransitivity()

#smallWorldProblem()
#testTrustTransitivity()
#print "transitivity complete"
#testTrustCombining()
#print "combining complete"



#usersX = getNodesXInDegree(150)
#print "Calculating the public opinion for %d users" %len(usersX.keys())
#calculateOpinionsAndWriteToFile(2, usersX, 1)
#print
#usersY = getNodesYInDegree(20)
#print "Calculating the public opinion for %d users" %len(usersY.keys())
#calculateOpinionsAndWriteToFile(2, usersY, 2)






