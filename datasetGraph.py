## advogato graph attempt 1

import networkx as nx
import matplotlib.pyplot as plt

names = open('advogato/ent.advogato.user.name', 'r')
edges = open('advogato/out.advogato', 'r')

namesList = []
lineArray = []
subGraph = []

for line in names:
	namesList.append(line)

for i in range(0,50):
	subGraph.append(namesList[i-1])

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



plt.figure(figsize=(10,10))


listOfNeighbors = []
#listOfNeighbors = subDG.neighbors(subDG[1])
"""for i in subDG.neighbors_iter(0)
	if i == 0:
		continue
	listOfNeighbors.append(i)

neighborsGraph = subDG.subgraph(listOfNeighbors)
nx.draw(neighborsGraph)
	


"""


pos=nx.spring_layout(subDG)
nx.draw_networkx_nodes(subDG, pos, node_size = 75)
nx.draw_networkx_edges(subMasterDG, pos)
nx.draw_networkx_edges(subJourneyerDG, pos, edge_color = 'g')
nx.draw_networkx_edges(subApprenticeDG, pos, edge_color = 'b')

plt.show()



names.close()
edges.close()



