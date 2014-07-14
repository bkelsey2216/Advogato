from EXP0 import readDotFile
from EXP0 import getTrustorsOfExactHop
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
				#propogation(transitivity)
				writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp4/Coupling.csv")
				XLevel = DG[node1][node2]['level']
				YLevel = DG[node2][node3]['level']
				ZLevel = DG[node1][node3]['level']
				writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp4/Propagation.csv")							

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
	

# This function selects random pairs of nodes and checks whether a path exists between them.
# If a path does exist, it computes the length of the shortest path and gets a list of nodes on
# the shortest path. The opinions along this path are then discounted into one final opinion
# connecting the original pair of nodes. The final opinion and path length are written into
# a line of a .csv file for Experiment 4 data analysis.
def makeOpinionFile():	
	pairsList = []
	#open and close file to make blank
	open('OutputExp4/opinionsList.csv', 'w').close()

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

				with open('OutputExp4/opinionsList.csv', 'a') as csvfile:
					toWrite = csv.writer(csvfile, delimiter = ',')
					toWrite.writerow([pathLength, pairOpinion[0], pairOpinion[1], pairOpinion[2], pairOpinion[3]])

if os.path.exists('OutputExp4') == False:
	print "Making the directory OutputExp4"
	os.mkdir("OutputExp4")

DG = readDotFile("master-graph.dot")

testCocitationCouplingAndTransitivity()

