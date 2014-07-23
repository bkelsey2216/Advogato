## Natalie Pollard & Brooke Kelsey

from GeneralMethods import distWrite
from GeneralMethods import readDotFile
from GeneralMethods import getNodeIntDict
#from GeneralMethods import getTrustorsOfExactHop
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
	statsArray = [0] * len(DG)

	#count the number of nodes node can reach
	for node in DG.nodes():
		numberOfNodesReachable = len(nx.single_source_shortest_path_length(DG,node, cutoff = numHops))
		statsArray[numberOfNodesReachable] += 1

	distWrite(statsArray, "OutputExp1/reachableDistribution" + str(numHops) + ".txt")

# Writes a file such that file[x] = y means that there are x nodes with an in degree of y
# in the graph
def writeInDegreeDistribution():
	statsArray = [0] * len(DG)

	for node in DG:		
		statsArray[DG.in_degree(node)] += 1

	distWrite(statsArray, "OutputExp1/inDegreeOfNodesDistribution.txt")

# Writes a file such that file[x] = y means that there are x nodes with an out degree of y
# in the graph
def writeOutDegreeDistribution():
	statsArray = [0] * len(DG)

	for node in DG:		
		statsArray[DG.out_degree(node)] += 1

	distWrite(statsArray, "OutputExp1/outDegreeOfNodesDistribution.txt")



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
# AdditionToPathLength is the additional hops which will be used to compute
# private opinions. Increasing it will significantly impact runtime
def writePublicAndPrivateOpinionsToFile(numHops, userDict, groupID, additionToPathLength=1):
	nodeIntDict = getNodeIntDict(DG)
	reverseDG = DG.reverse()

	with open('OutputExp1/' + str(groupID) + 'output.csv', 'wb') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		
		for node in userDict:
			print "For node " + node						

			# the public opinion is the comined opinion of all nodes 1 hop away
			publicOpinion = computePublicOpinion(node)
			print "The public opinion is " + str(publicOpinion)			

			# get trustors of exact hop
			# get a bfs edge generator of edges pointing to node
			dictOfPathLengths = nx.single_source_shortest_path_length(reverseDG, node, cutoff = numHops)
			trustorNodes = [x for x in dictOfPathLengths.keys() if dictOfPathLengths[x] == numHops]

			for trustor in trustorNodes:
				if trustor == node:
					print "Something has gone horribly wrong"

				subDG = nx.DiGraph()

				# fill subD with all the edges which occur in paths of length numHops + additionToPathLength
				# from trustor to node	
				path = nx.all_simple_paths(DG, source=trustor, target=node, cutoff=numHops + additionToPathLength)			
				for p in path:
					for i in range(0, len(p)-1):
						subDG.add_edge(p[i], p[i+1], level=DG[p[i]][p[i+1]]['level'])


				currentOpinion = TVSLAlgr(subDG, trustor, node, numHops + additionToPathLength, 0)
				#print trustor + "'s opinion of " + node + " is " + str(currentOpinion)
				# big file writing statement
				toWrite.writerow([groupID, nodeIntDict[node], userDict[node], 
				nodeIntDict[trustor], currentOpinion[0], currentOpinion[1], 
				currentOpinion[2], currentOpinion[3], publicOpinion[0], publicOpinion[1], 
				publicOpinion[2], publicOpinion[3]])


if os.path.exists('OutputExp1') == False:
	print "Making the directory OutputExp1"
	os.mkdir("OutputExp1")

DG = readDotFile("data.dot")


"""
writeReachableDistribution(1)
writeReachableDistribution(2)
writeReachableDistribution(3)
writeDegreeDistribution()
"""
usersX = getNodesXInDegree(150)
print "Calculating the public opinion for %d users" %len(usersX.keys())
writePublicAndPrivateOpinionsToFile(2, usersX, 1)
print
usersY = getNodesYInDegree(10)
print "Calculating the public opinion for %d users" %len(usersY.keys())
writePublicAndPrivateOpinionsToFile(2, usersY, 2)
