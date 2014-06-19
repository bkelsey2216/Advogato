## Natalie Pollard & Brooke Kelsey

import pygraphviz
import networkx as nx
import matplotlib.pyplot as plt
import string

#This code removes numerical values from the .dot file because 
#the networkx read_dot method does not play well with numerical values
def removeNumbers():
	f = open('advogato-graph-latest.dot', 'r')
	o = open('advogato-fixed-numbers.dot', 'w')

	for line in f:
		line = string.replace(line, "0","zero")
		line = string.replace(line, "1","one")
		line = string.replace(line, "2","two")
		line = string.replace(line, "3","three")
		line = string.replace(line, "4","four")
		line = string.replace(line, "5","five")
		line = string.replace(line, "6","six")
		line = string.replace(line, "7","seven")
		line = string.replace(line, "8","eight")
		line = string.replace(line, "9","nine")
		o.write(line)

removeNumbers()


