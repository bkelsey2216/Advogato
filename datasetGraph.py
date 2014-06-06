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


for line in edges:
	lineArray = line.split(' ', 3)

	#print line
	sourceNode = namesList[int(lineArray[0]) - 1]
	destNode = namesList[int(lineArray[1]) - 1]	
	DG.add_weighted_edges_from([(sourceNode, destNode, float(lineArray[2]))])

subDG = DG.subgraph(subGraph)

pos=nx.graphviz_layout(subDG,prog='twopi',args='')
plt.figure(figsize=(10,10))
nx.draw(subDG,pos,node_size=800,alpha=0.5,node_color="blue", with_labels=True)
plt.axis('equal')
plt.savefig('testGraph.png')
plt.show()

names.close()
edges.close()



