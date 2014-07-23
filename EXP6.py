import networkx as nx
from PageRankNibble_undirected import PageRankNibble 
import random
import csv
import os
from GeneralMethods import readDotFile 
from GeneralMethods import getTrustorsOfExactHop
from GeneralMethods import getTrusteesOfExactHop
from TVSL3 import TVSLAlgr #trust assess algr

if os.path.exists('OutputExp6') == False:
	print "Making the directory OutputExp6"
	os.mkdir("OutputExp6")
DG = readDotFile('data.dot')

Eps = 0.000001  #set up epsilon
alpha = 0.15  # set alpha

#pick up a nodes far enough from the seed
#so that the subgraph on which APPR run will 
#will be large enough

numHops = 4
rand = random.randint(0,len(DG.nodes())-1)
Seed = DG.nodes()[rand]
remoteSeed =  getTrustorsOfExactHop(DG, Seed, numHops)


while remoteSeed == 0 :
    Seed = DG.nodes()[rand]
    remoteSeed =  getTrustorsOfExactHop(DG, Seed, numHops)

PR = PageRankNibble(DG, Seed, alpha, Eps)
print "the length of PR is " + str(len(PR))
H = DG.subgraph(PR)

def withinCluster(DG, cluster, numHops = 2, additionToPathLength = 1, numberOfReps = 1000):
	with open('OutputExp6/WithinCluster.csv', 'w') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')

		currentRep = 0

		while currentRep < numberOfReps:
			# Choose a random node and a another random node IN THE CLUSTER which it trusts with min distance numHops
			node = random.choice(cluster.nodes())
			print "The node is " + str(node)
			trustees = getTrusteesOfExactHop(cluster, node, numHops)
			if trustees:

				trustee = random.choice(trustees)
				print "trustee " + str(trustee)

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
			print "The node is " + str(node)
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
			print "trustee " + str(trustee)

print "within"
withinCluster(DG, H, 2)
print "out"
outOfCluster(DG, H, 2)
print "done"

