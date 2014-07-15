from GeneralMethods import readDotFile
from GeneralMethods import getTrustorsOfExactHop
from GeneralMethods import writeTriangleOfTrust
import networkx as nx
import os
import csv
from TVSL3 import TVSLTran #transfer edge attributes to opinion
from TVSL3 import TVSLAlgr #trust assess algr
from TVSL3 import disc #trust assess algr
import random


# This method tests CoCitation, Coupling and Transitivity as
# outlined in the Matiri paper.
# All of these require a topolpology with egdes node -> node2,
# node -> node3 and node2 -> node3
# The only difference between the outputs is which node is 
# considdered X, Y and Z
def testCocitationCouplingAndTransitivity():
	#open the files and write nothing, clearing the file
	open('OutputExp4/CoCitation.csv', 'w').close()
	open('OutputExp4/Coupling.csv', 'w').close()
	open('OutputExp4/Propagation.csv', 'w').close()

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
				writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp4/CoCitation.csv")
				#coupling
				XLevel = DG[node2][node3]['level']
				YLevel = DG[node1][node3]['level']
				ZLevel = DG[node1][node2]['level']
				writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp4/Coupling.csv")
				#propogation			
				XLevel = DG[node1][node2]['level']
				YLevel = DG[node2][node3]['level']
				ZLevel = DG[node1][node3]['level']
				writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp4/Propagation.csv")							


	

# This function selects random pairs of nodes and checks whether a path exists between them.
# If a path does exist, it computes the length of the shortest path and gets a list of nodes on
# the shortest path. The opinions along this path are then discounted into one final opinion
# connecting the original pair of nodes. The final opinion and path length are written into
# a line of a .csv file for Experiment 4 data analysis.
def makeHighExpBeliefSample():	
	pairsList = []
	#open and close file to make blank
	open('OutputExp4/opinionsList.csv', 'w').close()

	# file format: [pairOpinion[0], pairOpinion[1], pairOpinion[2], pairOpinion[3], pathLength]

	#need a sample of 1000 opinions. ideally, running for 50000 iterations will produce a list
	# that has at least 1000 opinions with expected belief over 0.75
	for i in range(0, 10000):
		newPair = random.sample(DG.nodes(), 2)
		if newPair not in pairsList:

			if nx.has_path(DG, newPair[0], newPair[1]):
				pairOpnDG = nx.DiGraph()
				pathLength = nx.shortest_path_length(DG, newPair[0], newPair[1])
				paths = nx.all_simple_paths(DG, source=newPair[0], target=newPair[1], cutoff=pathLength+ 1)
				for path in paths:
					nodeList = []
					for i in range(0, len(path)-1):
						pairOpnDG.add_edge(path[i], path[i+1], level=DG[path[i]][path[i+1]]['level'])
				pairOpinion = TVSLAlgr(pairOpnDG, newPair[0], newPair[1], pathLength+1, 0)
				print pathLength
				print pairOpinion

				with open('OutputExp4/opinionsList.csv', 'a') as csvfile:
					toWrite = csv.writer(csvfile, delimiter = ',')
					toWrite.writerow([pathLength, pairOpinion[0], pairOpinion[1], pairOpinion[2], pairOpinion[3]])

if os.path.exists('OutputExp4') == False:
	print "Making the directory OutputExp4"
	os.mkdir("OutputExp4")

DG = readDotFile("master-graph.dot")

testCocitationCouplingAndTransitivity()
makeHighExpBeliefSample()

