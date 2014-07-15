## Natalie Pollard & Brooke Kelsey

from GeneralMethods import distWrite
from GeneralMethods import readDotFile
from GeneralMethods import getNodeIntDict
from GeneralMethods import getTrustorsOfExactHop
import networkx as nx
import os
import csv
from TVSL3 import TVSLTran #transfer edge attributes to opinion
from TVSL3 import TVSLAlgr #trust assess algr
from TVSL3 import comb #combining operation
from TVSL3 import disc

global DG

# This writes the file reachableDistribution + numHops + .txt such that
# file[x] = y means that there are x nodes that can reach exactly y other nodes
# within numHops
def writeReachableDistribution(numHops):
	statsArray = [0] * len(DG.nodes())

	for node in DG.nodes():
		listOfReachables = []
		getListOfNodesReachableInNHops(numHops, 0, listOfReachables, node)
		numberOfNodesReachable = len(listOfReachables)

		statsArray[numberOfNodesReachable] += 1

	distWrite(statsArray, "OutputExp1/reachableDistribution" + str(numHops) + ".txt")

# This method performs a recursive depth first search to add all the nodes within 
# numberOfHops of the node to the listOfReachables
# current depth should be set to zero
# listOfReachables should be an empty list
def getListOfNodesReachableInNHops(numberOfHops, currentDepth, listOfReachables, node):
	if currentDepth == numberOfHops:
		return listOfReachables
	
	for n in DG.neighbors(node):
		if not n in listOfReachables:
			listOfReachables.append(n)
			getListOfNodesReachableInNHops(numberOfHops, currentDepth+1, listOfReachables, n)

# Writes a file such that file[x] = y means that there are x nodes with an in degree of y
# in the graph
def writeDegreeDistribution():
	statsArray = [0] * len(DG.nodes())

	for node in DG:		
		statsArray[DG.in_degree(node)] += 1

	distWrite(statsArray, "OutputExp1/degreeOfNodesDistribution.txt")



## returns a dictionary of key=node:value=inDegree for all nodes in the graph
## having an inDegree *greater than or equal to the inDegree parameter
def getNodesXInDegree(inDegree):
	nodeListDict = {}
	for node in DG:
		if DG.in_degree(node) >= inDegree:
			nodeListDict[node] = DG.in_degree(node)

	return nodeListDict

## returns a dictionary of key=node:value=inDegree for all nodes in the graph
## having an inDegree *less than or equal to the inDegree parameter
def getNodesYInDegree(inDegree):
	nodeListDict = {}
	for node in DG:
		if DG.in_degree(node) <= inDegree and DG.in_degree(node) > 0:
			nodeListDict[node] = DG.in_degree(node)

	return nodeListDict



# Combine the opinions of the direct predecessors coming into the node
# and return the public opinion vector
def computePublicOpinion(node):
	predecessors = DG.predecessors(node)
	if len(predecessors) < 0:
		print "Error: cannot compute public opinion of a node with no predecessors"

	level = DG[predecessors[0]][node]['level']
	currentOpinion = TVSLTran(level)

	for i in range(1,len(predecessors)):
		level = DG[predecessors[i]][node]['level']
		currentOpinion = comb(TVSLTran(level), currentOpinion)

	return currentOpinion




# This method calls compute public opinion on all the users
# in userDict. It then calculates the opinion of each node exacly
# numHops away. It outputs these opinions in the format 
# [groupID (1 = X, 2 = Y); trusteeID; inDegree of trustee; trustorID; trustor's opinion; public opinion]
# to the file groupID + "output.csv"
def calculateOpinionsAndWriteToFile(numHops, userDict, groupID):
	# This variable is the additional length wich can be added to numhops
	# (The one you suggested be 3 in your instructions)
	# Altering this variable will significantly impact runtime
	additionToPathLength = 1

	nodeIntDict = getNodeIntDict(DG)

	with open('OutputExp1/' + str(groupID) + 'output.csv', 'wb') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		
		for node in userDict:
			print "For node " + node						

			# the public opinion is the comined opinion of all nodes 1 hop away
			publicOpinion = computePublicOpinion(node)
			print "The public opinion is " + str(publicOpinion)			
			
			# trustor nodes is the list of nodes with shortest path numHops to node
			trustorNodes = getTrustorsOfExactHop(DG, node, numHops)

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


if os.path.exists('OutputExp1') == False:
	print "Making the directory OutputExp1"
	os.mkdir("OutputExp1")

DG = readDotFile("master-graph.dot")

writeReachableDistribution(1)
writeReachableDistribution(2)
writeReachableDistribution(3)
writeDegreeDistribution()

usersX = getNodesXInDegree(150)
print "Calculating the public opinion for %d users" %len(usersX.keys())
calculateOpinionsAndWriteToFile(2, usersX, 1)
print
usersY = getNodesYInDegree(20)
print "Calculating the public opinion for %d users" %len(usersY.keys())
calculateOpinionsAndWriteToFile(2, usersY, 2)