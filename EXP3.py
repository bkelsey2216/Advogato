from GeneralMethods import readDotFile
import networkx as nx
import os
import csv
from TVSL3 import TVSLTran #transfer edge attributes to opinion
from TVSL3 import TVSLAlgr #trust assess algr
import random


# This function traverses all nodes in the graph to find pairs A,B such that A->B and B->A are
# both edges that exist in the dataset. Taking care to not repeat pairs, the function appends these
# pairs to a 'listofSymms'. It then forms a sample population of 1000 such symmetrical relationships
# using random.sample, and returns this sublist to the function caller.
def findSymmetricalTrust(numberOfReps=1000):
	listofSymms = []
	for node in DG:
		listofNeighbors = DG.neighbors(node)
		for neighbor in listofNeighbors:
			if DG.has_edge(neighbor, node):
				newPair = [node, neighbor]
				checknewPair = [neighbor, node]
				if (newPair not in listofSymms) and (checknewPair not in listofSymms):
					listofSymms.append(newPair)

	sampleRelationships = random.sample(listofSymms, numberOfReps)

	return sampleRelationships



# This function takes the random sample of mutual trusting nodes, finds their respective opinions
# by indexing into the graph edge weights, transforms these edge weights into an opinion using TVSLTran,
# and writes these two opinions onto one line of a .csv file. This .csv file will be the input to
# MATLAB code computing the expected belief for a CDF.
def computeTrustDifference():
	#open the file and write nothing, clearing the file
	open('OutputExp3/symmetricTrust.csv', 'w').close()
	relationships = findSymmetricalTrust()
	for pair in relationships:
		levelAB = DG[pair[0]][pair[1]]['level']
		levelBA = DG[pair[1]][pair[0]]['level']
		trustAB = TVSLTran(levelAB)
		trustBA = TVSLTran(levelBA)

		with open('OutputExp3/symmetricTrust.csv', 'a') as csvfile:
			toWrite = csv.writer(csvfile, delimiter = ',')
			toWrite.writerow([trustAB[0], trustAB[1], trustAB[2], trustAB[3], trustBA[0], trustBA[1], trustBA[2]])




# This method randomly finds 1000 pairs of nodes with shortest path numHops between 
# them. It calculates the trust between these nodes using 3VSL. It outputs the resulting 
# trust vector to str(numHops) + distance.csv
def decayOfTrustVsShortestDistance(numHops, additionToPathLength = 1, numberOfReps = 1000):
	numberOfPairs = 0

	with open("OutputExp3/" + str(numHops) + 'distance.csv', 'wb') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		
		while numberOfPairs < numberOfReps:
			node = random.choice(DG.nodes())
			
			# get trustors of exact hop
			# get a bfs edge generator of edges pointing to node
			bfsGenerator = nx.bfs_edges(DG,node, reverse = True)
			trustorNodes = []

			for edge in bfsGenerator:
				pathLength = nx.shortest_path_length(DG, edge[1], node)
				if pathLength > numHops:
					break
				elif pathLength == numHops:
					trustorNodes.append(edge[1])

			if trustorNodes:		
				trustor = random.choice(trustorNodes)
				# fill subDG with all the edges which occur in paths of length numHops + additionToPathLength
				subDG = nx.DiGraph()	
				path = nx.all_simple_paths(DG, source=trustor, target=node, cutoff=numHops + additionToPathLength)
				for p in path:
					for i in range(0, len(p)-1):
						subDG.add_edge(p[i], p[i+1], level=DG[p[i]][p[i+1]]['level'])
				
				currentOpinion = TVSLAlgr(subDG, trustor, node, numHops + additionToPathLength, 0)
				#print trustor + "'s opinion of " + node + " is " + str(currentOpinion)
				
				# big file writing statement
				toWrite.writerow([currentOpinion[0], currentOpinion[1], 
				currentOpinion[2], currentOpinion[3]])

				numberOfPairs += 1

DG = readDotFile("data.dot")

if os.path.exists('OutputExp3') == False:
	print "Making the directory OutputExp3"
	os.mkdir("OutputExp3")

#computeTrustDifference()
decayOfTrustVsShortestDistance(1)
decayOfTrustVsShortestDistance(2)
#decayOfTrustVsShortestDistance(3)
#decayOfTrustVsShortestDistance(4)
