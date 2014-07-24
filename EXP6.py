import networkx as nx
from PageRankNibble_undirected import PageRankNibble 
import random
import csv
import os
from GeneralMethods import readDotFile 
from GeneralMethods import getTrustorsOfExactHop
from GeneralMethods import getTrusteesOfExactHop
from TVSL3 import TVSLAlgr #trust assess algr
from TVSL3 import TVSLTran
from runPRN import runPRN

global externalDG
global clusterDG
global DG


def withinCluster(DG, cluster, numHops = 2, additionToPathLength = 1, numberOfReps = 1000):
	with open('OutputExp6/WithinCluster.csv', 'w') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')

		currentRep = 0

		while currentRep < numberOfReps:
			# Choose a random node and a another random node IN THE CLUSTER which it trusts with min distance numHops
			node = random.choice(cluster.nodes())
			trustees = getTrusteesOfExactHop(cluster, node, numHops)
			if trustees:

				trustee = random.choice(trustees)

				#calcuate the opinion from node to trustee and write to a file
				subDG = nx.DiGraph()	
				path = nx.all_simple_paths(DG, source=node, target=trustee, cutoff=numHops + additionToPathLength)
				for p in path:
					for i in range(0, len(p)-1):
						subDG.add_edge(p[i], p[i+1], level=DG[p[i]][p[i+1]]['level'])
				
				currentOpinion = TVSLAlgr(subDG, node, trustee, numHops + additionToPathLength, 0)
				
				toWrite.writerow([currentOpinion[0],currentOpinion[1],currentOpinion[2],currentOpinion[3]])
				currentRep += 1

def outOfCluster(DG, cluster, numHops = 2, additionToPathLength = 1, numberOfReps = 1000):
	with open('OutputExp6/OutOfCluster.csv', 'w') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')

		currentRep = 0

		while currentRep < numberOfReps:
			# Choose a random node and a another random node which it trusts with min distance numHops
			node = random.choice(cluster.nodes())
			trustees = getTrusteesOfExactHop(DG, node, numHops)
			if not trustees:
				continue

			trustee = random.choice(trustees)
			
			# Disregrard any trustees in the cluster
			if trustee in cluster:
				continue

			#calcuate the opinion from node to trustee and write to a file
			subDG = nx.DiGraph()	
			path = nx.all_simple_paths(DG, source=node, target=trustee, cutoff=numHops + additionToPathLength)
			for p in path:
				for i in range(0, len(p)-1):
					subDG.add_edge(p[i], p[i+1], level=DG[p[i]][p[i+1]]['level'])
			
			currentOpinion = TVSLAlgr(subDG, node, trustee, numHops + additionToPathLength, 0)
			
			toWrite.writerow([currentOpinion[0],currentOpinion[1],currentOpinion[2],currentOpinion[3]])
			currentRep += 1

def pickRandEdges():
	global externalDG
	global clusterDG
	open('OutputExp6/clusterOpinions.csv', 'w').close()
	open('OutputExp6/nonClusterOpinions.csv', 'w').close()

	print 'creating Cluster graph with PRN'
	clusterDG = runPRN()
	print 'creating nonCluster graph'
	externalDG = readDotFile('advogato-graph-latest.dot')
	clusterEdges = clusterDG.edges()
	clusterNodes = clusterDG.nodes()
	externalDG.remove_edges_from(clusterEdges)
	externalDG.remove_nodes_from(clusterNodes)

	externalEdges = externalDG.edges()

	for i in range(0,1000):
		if len(clusterEdges) < 2:
			print "cluster too small to sample from, aborting..."
			break
		randClusterEdge = random.sample(clusterEdges, 1)
		randExtEdge = random.sample(externalEdges, 1)

		clusterOpn = TVSLTran(clusterDG[randClusterEdge[0][0]][randClusterEdge[0][1]]['level'])
		externalOpn = TVSLTran(externalDG[randExtEdge[0][0]][randExtEdge[0][1]]['level'])


		with open('OutputExp6/clusterOpinions.csv', 'a') as csvfile:
			toWrite = csv.writer(csvfile, delimiter = ',')
			toWrite.writerow([clusterOpn[0], clusterOpn[1], clusterOpn[2], clusterOpn[3]])

		with open('OutputExp6/nonClusterOpinions.csv', 'a') as csvfile:
			toWrite = csv.writer(csvfile, delimiter = ',')
			toWrite.writerow([externalOpn[0], externalOpn[1], externalOpn[2], externalOpn[3]])


if os.path.exists('OutputExp6') == False:
	print "Making the directory OutputExp6"
	os.mkdir("OutputExp6")


DG = readDotFile('advogato-graph-latest.dot')
H = runPRN()

pickRandEdges()

print "within"
withinCluster(DG, H, 2)
print "out"
outOfCluster(DG, H, 2)
print "done"

