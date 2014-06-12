#!/usr/bin/python

import networkx as nx
import numpy as np
from TVSL3 import TVSLTran #transfer edge attributes to opinion

from TVSL3 import TVSLAlgr #trust assess algr
from TVSL3 import TVSLExp #compute expected belief
from TVSL3 import comb #combining operation

MaxHop = 2
#f= '/home/loenix/Documents/MyScript/test' 
#rf= '/home/loenix/Documents/MyScript/testresult_2014-03-16_2002-01-14_2hp_old_norm'  #result file

f = 'testFile'
rf = 'testResultFile'
result= 'tmpFile'  #tmp file

rdfpre = 'advogato-graph-latest.dot'   # data set


G=nx.DiGraph(nx.read_dot(rdfpre))


nnum = len(G.nodes())
print(nnum)
enum = len(G.edges())
print(enum)



G.remove_edges_from(G.selfloop_edges())


ff = open(f,'wr+')
ffr = open(rf,'wr+')

edgeNum = 1000000
edgeCount = 0
Grev = G.reverse()

elist = G.edges()      #find those edges
G_int = nx.convert_node_labels_to_integers(G,label_attribute='old_name')  #transfer node names to numbers
intnlist = G_int.nodes()

for e in elist:
    Gmini=nx.DiGraph()     #initiate a mini subgraph






#Now begin to calculate paths from src to dst 

    path = nx.all_simple_paths(G, source=e[0], target=e[1], cutoff = MaxHop)   #filter out all paths from src to dst with in MaxHop
    
    for p in path:

        ff.write("{0}\n".format(p))

        for i in range(0,len(p)-1):
            ff.write("{0},{1}\n".format(p[i],p[i+1]))
            Gmini.add_edge(p[i],p[i+1],level=G[p[i]][p[i+1]]['level'],color='red')      #Use the paths obtained above to form a sub graph

    if Gmini:

        Nnum = Gmini.number_of_nodes()
        Enum = Gmini.number_of_edges()
        GminiR = Gmini.reverse()
        
  
                                      #transfer edge attributes of 1 hop ground truth to opinion
    
        curHop = 0
        finalOpn =  TVSLAlgr(GminiR, e[1], e[0], MaxHop, curHop)   #run assess trust on the subgraph to get computational opinion 
             
        if TVSLExp(finalOpn) > 0:
            print "printing final opinion"
            print( TVSLExp(finalOpn))
            print "printing edge count??"
            print( edgeCount)

            
            for n in intnlist:
                if G_int.node[n]['old_name'] == e[0]:
                    e_num_0 = n
                if G_int.node[n]['old_name'] == e[1]:
                    e_num_1 = n
            ffr.write("{0},{1},{2},{3},{4},{5},{6},{7},{8} \n"      #write result to result file
                      .format(TVSLExp(finalOpn),finalOpn[0],finalOpn[1],finalOpn[2],finalOpn[3],
                              e_num_0,e_num_1,Enum,Nnum))
    #B = nx.bfs_tree(Gmini,1)
    #for b in B:
       # print(b)
     
     

            
        
        
            
   #  "'{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}'".format(softname, procversion, int(percent), exe, description, company, procurl)
     
   # ff.write("{0}\n".format(list(path)))

     


