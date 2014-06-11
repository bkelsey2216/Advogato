import pygraphviz
import networkx as nx
import matplotlib.pyplot as plt


myGraph = nx.read_dot('exampleDotFile.dot')
nx.draw(myGraph)

print nx.get_edge_attributes(myGraph,'level')

plt.show()