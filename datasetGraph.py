## advogato graph attempt 1

import networkx as nx
import matplotlib.pyplot as plt

#This method performs a recursive depth first search to add all the nodes within a 
#specified distance of the specified node

#returns a list containing all the nodes within numberOfHops 
def getReachableInNHops(numberOfHops, currentDepth, listOfRechables, node):
	if currentDepth == numberOfHops:
		return listOfRechables
	
	for n in subDG.neighbors(node):
		if not n in listOfRechables:
			#print "appending %s" % n
			listOfRechables.append(n)
			getReachableInNHops(numberOfHops, currentDepth+1, listOfRechables, n)




names = open('advogato/ent.advogato.user.name', 'r')
edges = open('advogato/out.advogato', 'r')

namesList = []
lineArray = []
subGraph = []

for line in names:
	namesList.append(line)
for i in range(0,50):
	subGraph.append(namesList[i-1])


#subGraph = namesList;

DG = nx.DiGraph()
masterDG = nx.DiGraph()
journeyerDG = nx.DiGraph()
apprenticeDG = nx.DiGraph()


for line in edges:
	lineArray = line.split(' ', 3)

	sourceNode = namesList[int(lineArray[0]) - 1]
	destNode = namesList[int(lineArray[1]) - 1]
	rank = float(lineArray[2])
	DG.add_weighted_edges_from([(sourceNode, destNode, rank)])

	if rank == 1:
		masterDG.add_weighted_edges_from([(sourceNode, destNode, rank)])
	elif rank == .8:
		journeyerDG.add_weighted_edges_from([(sourceNode, destNode, rank)])
	elif rank == .6:
		apprenticeDG.add_weighted_edges_from([(sourceNode, destNode, rank)])

subDG = DG.subgraph(subGraph)
subMasterDG = masterDG.subgraph(subGraph)
subJourneyerDG = journeyerDG.subgraph(subGraph)
subApprenticeDG = apprenticeDG.subgraph(subGraph)

plt.figure(figsize=(9,9))


listOfRechables = []
node = subDG.nodes()[16]
numHops = 3
listOfRechables.append(node)
print "the start node is %s" %node

#getReachableInNHops(numberOfHops, depth, listOfRechables, node)
getReachableInNHops(numHops, 0, listOfRechables, node)

reachableWithin3HopsGraph  = subDG.subgraph(listOfRechables)
#nx.draw(reachableWithin3HopsGraph)
print "The nodes reachable within %d hops of %s" %(numHops, node)
print listOfRechables
print "The length of the list is %d" %len(listOfRechables)


pos=nx.random_layout(subDG)
nx.draw_networkx_nodes(subDG, pos, node_size = 75)
nx.draw_networkx_edges(subMasterDG, pos)
nx.draw_networkx_edges(subJourneyerDG, pos, edge_color = 'g')
nx.draw_networkx_edges(subApprenticeDG, pos, edge_color = 'b')
nx.draw_networkx_labels(subDG, pos)

plt.show()



names.close()
edges.close()



