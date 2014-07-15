## Natalie Pollard & Brooke Kelsey
from GeneralMethods import readDotFile

import networkx as nx
import os
import csv
from TVSL3 import TVSLTran #transfer edge attributes to opinion
from TVSL3 import TVSLAlgr #trust assess algr
from TVSL3 import disc
from GeneralMethods import distWrite
import random

global DG

######### The funcitonality of this method is now included in
######### testCocitationCouplingAndTransitivity() of EXP4

# /->B->\
#A------>D
# Finds all the paths in the graph with the topology
# A -> D and A -> B -> D.
# Write the trust vectors to the output file 
# PropogationOutput.csv
# in the order X (A->B), Y (B->D), Z (A->D)
def testTrustPropogation():
	#open the file and write nothing, clearing the file
	open('OutputExp2/PropogationOutput.csv', 'w').close()
	for D in DG.nodes():
		for A in DG.predecessors(D):
			allPaths = nx.all_simple_paths(DG,A,D,2)
			for path in allPaths:
				if len(path) == 3:
					writeForPropogation(path)


# helper method for testTrustPropogation to calculate the 
# trust vectors and write the vectors to the file
def writeForPropogation(path):
	XLevel = DG[path[0]][path[1]]['level']
	YLevel = DG[path[1]][path[2]]['level']
	ZLevel = DG[path[0]][path[2]]['level']

	XOpinion = TVSLTran(XLevel)
	YOpinion = TVSLTran(YLevel)
	ZOpinion = TVSLTran(ZLevel)

	with open('OutputExp2/PropogationOutput.csv', 'a') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		toWrite.writerow([XOpinion[0], XOpinion[1], XOpinion[2], XOpinion[3], 
		YOpinion[0], YOpinion[1], YOpinion[2], YOpinion[3], ZOpinion[0], 
		ZOpinion[1], ZOpinion[2], ZOpinion[3]])

# /->B->\
#A------>D
# \->C->/
# Finds all the nodes A and D in the graph with the topology
# A->D and A->B->D and A->C->D where B != C
# Write the trust vectors to the output file 
# ComposingOutput.csv
# in the order: X (disc(A->B, B->D)), Y (disc(A->C, C->D)), Z (A->D)
def testTrustComposing(numberOfReps=1000):
	#open the file and write nothing, clearing the file
	open('OutputExp2/ComposingOutput.csv', 'w').close()
	composingCounter = 0
	while composingCounter < numberOfReps:
		D = random.choice(DG.nodes())
		if DG.predecessors(D):
			A = random.choice(DG.predecessors(D))

			#generator for all paths with 2 or less edges
			allPaths = nx.all_simple_paths(DG, A, D, 2)
			#List of all paths with exactly 2 egdes
			pathsOfLengthList = [p for p in allPaths if len(p) == 3]
			
			#if the correct topology is present
			if len(pathsOfLengthList) >= 2:
				paths = random.sample(pathsOfLengthList,2)
				writeForComposing(paths[0],paths[1])
				composingCounter+=1


# helper method for testTrustCombining to calculate the 
# trust vectors and write the vectors to the file
def writeForComposing(path1, path2):
# output file = ComposingOutput.csv

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

	with open('OutputExp2/ComposingOutput.csv', 'a') as csvfile:
		toWrite = csv.writer(csvfile, delimiter = ',')
		toWrite.writerow([XOpinion[0], XOpinion[1], XOpinion[2], XOpinion[3], 
		YOpinion[0], YOpinion[1], YOpinion[2], YOpinion[3], ZOpinion[0], 
		ZOpinion[1], ZOpinion[2], ZOpinion[3]])

# Creates a distribution of the shortest distance between nodes
# Samples 1000 nodes
# file[0] contains the number of nodes where no path exists
def smallWorldProblem(numberOfReps=1000):
	distribution = []
	for i in range(0,50):
		distribution.append(0)

	for source in DG.nodes()[0:numberOfReps]:
		for D in DG.nodes():
			if source != D:
				if nx.has_path(DG,source,D) == False:
					distribution[0] +=1
				else:
					distribution[nx.shortest_path_length(DG, source, D)] +=1

	distWrite(distribution,"OutputExp2/smallworld.txt")




DG = readDotFile("data.dot")

if os.path.exists('OutputExp2') == False:
	print "Making the directory OutputExp2"
	os.mkdir("OutputExp2")

#testTrustPropogation()
print "okay"
testTrustComposing()
print "yay"
#smallWorldProblem()



