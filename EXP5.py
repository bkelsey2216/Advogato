from GeneralMethods import readDotFile
from GeneralMethods import writeTriangleOfTrust
import networkx as nx
import os
from TVSL3 import TVSLTran #transfer edge attributes to opinion
from TVSL3 import TVSLAlgr #trust assess algr
import random

global oldDG
global newDG


# Returns the nodes of a triangle in newDG
# where A -> B, A -> C, B -> C
def findRandomTriangle():
	while True:
		rand = random.randint(0,len(newDG.nodes())-1)
		A = newDG.nodes()[rand]
		neighbors = newDG.neighbors(A)
		if len(neighbors) > 2:
			rand1 = random.randint(0,len(neighbors)-1)
			rand2 = random.randint(0,len(neighbors)-1)
			
			#make sure rand1 != rand2
			while rand1 == rand2:
				rand2 = random.randint(0,len(neighbors)-1)
			B = neighbors[rand1]
			C = neighbors[rand2]

			#if the correct topology is present
			#ie. there exist edges
			# A -> B
			# A -> C
			# B -> C
			if newDG.has_edge(B,C):
				return (A,B,C)

# This method finds triangles which have the form A -> B, A -> C, B -> C
# in newDG but are missing exactly one of these edges in oldDG
# It writes the trust vector of the missing edge to the apropriate file
# It does this until there are 1000 examples of this toplogy in 
# each file
# May contain the same three nodes repeated many times
def testCocitationCouplingAndTransitivityOverTime():
	#open the files and write nothing, clearing the file
	open('OutputExp4/CoCitation.csv', 'w').close()
	open('OutputExp4/Coupling.csv', 'w').close()
	open('OutputExp4/Propagation.csv', 'w').close()

	desiredTriangles = 1000
	cocitationCounter = 0
	couplingCounter = 0
	propogationCounter = 0

	while (cocitationCounter < desiredTriangles or couplingCounter < desiredTriangles 
			or propogationCounter < desiredTriangles):

		(A, B, C) = findRandomTriangle()
		
		if (oldDG.has_edge(A,B) and (oldDG.has_edge(A,C) == False) and 
			oldDG.has_edge(B,C) and propogationCounter < desiredTriangles):
			print "prop"
			propogationCounter+=1
			XLevel = newDG[A][B]['level']
			YLevel = newDG[B][C]['level']
			ZLevel = newDG[A][C]['level']
			writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp5/Propagation.csv")

		elif (oldDG.has_edge(A,B) and oldDG.has_edge(A,C) and 
			(oldDG.has_edge(B,C) == False) and cocitationCounter < desiredTriangles):
			print "cocitation"
			cocitationCounter+=1
			XLevel = newDG[A][B]['level']
			YLevel = newDG[A][C]['level']
			ZLevel = newDG[B][C]['level']
			writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp5/CoCitation.csv")
		

		elif ((oldDG.has_edge(A,B)==False) and oldDG.has_edge(A,C) and 
			oldDG.has_edge(B,C) and couplingCounter < desiredTriangles):
			print "couple"
			couplingCounter+=1
			XLevel = newDG[B][C]['level']
			YLevel = newDG[A][C]['level']
			ZLevel = newDG[A][B]['level']
			writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp5/Coupling.csv")

	

if os.path.exists('OutputExp5') == False:
	print "Making the directory OutputExp5"
	os.mkdir("OutputExp5")

oldDG = readDotFile("old.dot")
newDG = readDotFile("data.dot")

newDG = newDG.subgraph(oldDG.nodes())
testCocitationCouplingAndTransitivityOverTime()
