import networkx as nx
#import numpy as np
#import numpy as np
#from Operator import disc
#from Operator import comb
from PageRankNibble_undirected import PageRankNibble 
import random
from GeneralMethods import readDotFile 
from GeneralMethods import getTrustorsOfExactHop

def runPRN():
	#DG = readDotFile('/home/loenix/Documents/advogato_graph/advogato-graph-2014-03-16.dot')
	DG = readDotFile('advogato-graph-latest.dot')
	#DG = nx.DiGraph(nx.read_dot('/home/loenix/Documents/advogato_graph/advogato-graph-2014-03-16.dot'))

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

	#now got a seed which has 4 hop neighbor, run APPR

	#print('seed is:' + Seed)
	#print('nb of seed is: ' + str(DG.neighbors(Seed)))
	#since the algr works on undirected graph
	DG.to_undirected()
	PR = PageRankNibble(DG, Seed, alpha, Eps)
	#using the ranked nodes to form a subgraph. 
	H = DG.subgraph(PR)
	nx.write_dot(H, 'pprResult.dot')
	return H
