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
		A = random.choice(newDG.nodes())
		neighbors = newDG.neighbors(A)
		if len(neighbors) >= 2:
			(B,C) = random.sample(neighbors,2)
			if newDG.has_edge(B,C):
				return (A,B,C)

# This method finds triangles which have the form A -> B, A -> C, B -> C
# in newDG but are missing exactly one of these edges in oldDG
# It writes the trust vector of the missing edge to the coupling file
def testCouplingOverTime(desiredTriangles = 1000):
	open('OutputExp5/Coupling.csv', 'w').close()
	couplingCounter = 0
	while couplingCounter < desiredTriangles:
		(A, B, C) = findRandomTriangle()
		if (oldDG.has_edge(A,B)==False) and oldDG.has_edge(A,C) and oldDG.has_edge(B,C):
			couplingCounter+=1
			XLevel = newDG[B][C]['level']
			YLevel = newDG[A][C]['level']
			ZLevel = newDG[A][B]['level']
			writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp5/Coupling.csv")

# This method finds triangles which have the form A -> B, A -> C, B -> C
# in newDG but are missing exactly one of these edges in oldDG
# It writes the trust vector of the missing edge to the cocitation file
def testCocitationOverTime(desiredTriangles = 1000):
	open('OutputExp5/CoCitation.csv', 'w').close()
	cocitationCounter = 0
	while cocitationCounter < desiredTriangles: 
		(A, B, C) = findRandomTriangle()
		if oldDG.has_edge(A,B) and oldDG.has_edge(A,C) and (oldDG.has_edge(B,C) == False):
			cocitationCounter+=1
			XLevel = newDG[A][B]['level']
			YLevel = newDG[A][C]['level']
			ZLevel = newDG[B][C]['level']
			writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp5/CoCitation.csv")

# This method finds triangles which have the form A -> B, A -> C, B -> C
# in newDG but are missing exactly one of these edges in oldDG
# It writes the trust vector of the missing edge to the propogation file
def testTransitivityOverTime(desiredTriangles = 1000):
	open('OutputExp5/Propagation.csv', 'w').close()
	propogationCounter = 0
	while  propogationCounter < desiredTriangles:
		(A, B, C) = findRandomTriangle()
		if oldDG.has_edge(A,B) and (oldDG.has_edge(A,C) == False) and oldDG.has_edge(B,C):
			propogationCounter+=1
			XLevel = newDG[A][B]['level']
			YLevel = newDG[B][C]['level']
			ZLevel = newDG[A][C]['level']
			writeTriangleOfTrust(XLevel,YLevel,ZLevel,"OutputExp5/Propagation.csv")


# This method finds triangles which have the form A -> B, A -> C, B -> C
# in newDG but are missing exactly one of these edges in oldDG
# It writes the trust vector of the missing edge to the apropriate file
# It does this until there are 1000 examples of this toplogy in 
# each file
# May contain the same three nodes repeated many times
# This is three times faster than finding all 3 different topologies individually
def testCocitationCouplingAndTransitivityOverTime(desiredTriangles = 1000):
	#open the files and write nothing, clearing the file
	open('OutputExp5/Coupling.csv', 'w').close()
	open('OutputExp5/CoCitation.csv', 'w').close()
	open('OutputExp5/Propagation.csv', 'w').close()

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
