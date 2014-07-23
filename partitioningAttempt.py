## Natalie Pollard & Brooke Kelsey

import networkx as nx
import pygraphviz
import matplotlib.pyplot as plt
from collections import defaultdict
from decimal import Decimal
import csv
from TVSL3 import TVSLTran #transfer edge attributes to opinion
from TVSL3 import TVSLAlgr #trust assess algr
from TVSL3 import TVSLExp #compute expected belief
from TVSL3 import comb #combining operation
from TVSL3 import disc
import random
import scipy as sp
import numpy as np
import operator
from  GeneralMethods import readDotFile 
from  GeneralMethods import getNodeIntDict

global DG
global nodeIntDict

#I still do not know what alpha and beta should be set to
def localPartitioningAttempt(alpha, beta, node):
	gamma = alpha + beta - alpha * beta
	global nodeIntDict
	nodeIntDict = getNodeIntDict(DG)
	
	#This returns the transition matrix, which I think is the random walk matrix
	M = nx.google_matrix(DG)
	print "M"
	print M
	print "about to page rank"

	# Compute the two global page rank vectors
	prBeta  = nx.pagerank(DG, alpha=beta)
 	prGamma = nx.pagerank(DG, alpha=gamma)

 	#starting vector for local page rank with all probability on node
 	localDict = dict.fromkeys(DG.nodes(), 0)
 	localDict[node] = 1

 	localPR = nx.pagerank(DG, alpha=gamma, nstart=localDict, personalization=localDict)
 	
 	#linear combination
 	#this would maybe be faster if I used actual arrays instead of dictionaries
 	p = {}
 	for key in localPR.keys():
 		p[key] = (alpha/gamma)*localPR[key] + (((1-alpha)*beta)/gamma)*prGamma[key]
 		p[key] = p[key]/prBeta[key]
 	
 	#create a list of tuples sorted in non-increasing order by value
 	sortedP = sorted(p.iteritems(), key = operator.itemgetter(1), reverse=True)
 	sortedLocalPR = sorted(localPR.iteritems(), key = operator.itemgetter(1), reverse=True)
 	print "node is " + str(node)
 	print "sortedLocalPR is "
  	print sortedLocalPR[0:20]	
 	print "sortedP" 
 	print sortedP[0:20]

 	print "Conductance Loop"
 	S = []
 	notS = DG.nodes()
 	j = 0
 	S.append(sortedP[j][0])
 	notS.remove(sortedP[j][0])
 	minConducance = calculateConductance(S, notS)
 	minJ = j
 	for j in range(2,len(sortedP)):
 		S.append(sortedP[j][0])
 		notS.remove(sortedP[j][0])
 		tempConductance = calculateConductance(S, notS)
 		#print "cond " + str(tempConductance)
 		if tempConductance < minConducance:
 			minConducance = tempConductance
 			minJ = j
 	print minJ
 	print minConducance


 	minSet = sortedP[0:j]
 	print "minset"
 	print minSet
 	print "length of minset " + str(len(minSet))
 	return minSet 	
 	"""
 	pos=nx.spring_layout(DG)
 	nx.draw_networkx_edges(DG,pos)
 	nx.draw_networkx_nodes(DG,node_color=p.)
 	"""


def calculateConductance(S, notS):
	global nodeIntDict
	#print "M"
	#print M
	top = 1
	for i in S:
		for j in notS:
			#top += prBeta[i]*M[nodeIntDict[i],nodeIntDict[j]]
			if (i,j) in DG.edges():
				top += 1
	#print "S "+ str((S))
	#print "notS "+ str((notS))

	bottom = 1
	for i in S:
		for j in S:
			if(i,j) in DG.edges():
				bottom += 1

	
	conductance = top/bottom
	print "conductance " + str(conductance)
	return conductance



def makeAToyGraph():
	return nx.gnm_random_graph(50, 0, directed = True)

print "okay"
#DG = readDotFile("data.dot")
DG = makeAToyGraph()
#DG.add_edge(0,1)
#DG.add_edge(1,2)
print DG.edges()

print "okay"
localPartitioningAttempt(.5,.85,DG.nodes()[0])



