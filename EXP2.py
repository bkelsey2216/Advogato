## Natalie Pollard & Brooke Kelsey
from EXP0 import readDotFile

import networkx as nx
import os
import csv
from TVSL3 import TVSLTran #transfer edge attributes to opinion
from TVSL3 import TVSLAlgr #trust assess algr
from TVSL3 import disc
from EXP0 import distWrite

global DG


# Finds all the paths in the graph with the topology
# start -> dest and start -> middle -> dest.
# Write the trust vectors to the output file 
# PropogationOutput.csv
# in the order X (start->middle), Y (middle->dest), Z (start->dest)
def testTrustPropogation():
	#open the file and write nothing, clearing the file
	open('OutputExp2/PropogationOutput.csv', 'w').close()
	for dest in DG.nodes():
		for pred in DG.predecessors(dest):
			allPaths = nx.all_simple_paths(DG,pred,dest,2)
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


# Finds all the nodes start and dest in the graph with the topology
# start -> dest and start -> mid1 -> dest and start->mid2->dest where mid1 != mid2
# Write the trust vectors to the output file 
# ComposingOutput.csv
# in the order: X (disc(start->mid1, mid1->dest)), Y (disc(start->mid2, mid2->dest)), Z (start->dest)
def testTrustComposing():
	#open the file and write nothing, clearing the file
	open('OutputExp2/ComposingOutput.csv', 'w').close()
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

				writeForComposing(path1,path2)


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

	distWrite(distribution,"OutputExp2/smallworld.txt")




DG = readDotFile("master-graph.dot")

if os.path.exists('OutputExp2') == False:
	print "Making the directory OutputExp2"
	os.mkdir("OutputExp2")

testTrustPropogation()
testTrustComposing()
smallWorldProblem()



