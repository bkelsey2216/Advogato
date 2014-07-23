import networkx as nx




# now run the pagerank-nibble
# The algorithm is written referring to: 
#Algr 1 and 2 in "SoK: The Evolution of Sybil Defense via Social Networks"
#Algr on p6 in "Local Graph Partitioning using PageRank Vectors"


def PageRankNibble(LoadGraph, seed, alpha, eps):
    
    ppr={}  #persinalized page rank
    r = {}   #residual vector
    for m in LoadGraph.nodes():
        ppr[m] = 0
        r[m] = 0
    Queue = []  #nodes set in which r(x) >= epsilon*(d(x))
    finalResult = [] # final result
  
    # insert the initial seed, set its residual value as 1
    Queue.append(seed)
    r[seed] = 1
    while Queue:
        for n in Queue:
            #print('current  node being processed is: ' + n)
            while r[n] >= eps*LoadGraph.degree(n):
                # if its residual value is greater than threshold, recall push operation
                ppr, r = Push(ppr,r,n, alpha, LoadGraph)
                # insert the neighbor nodes whose residual value became greater than threshold when applying push operation
                # to their parent node into queue. 
                for nb in LoadGraph.neighbors(n):
                    if r[nb] >=  eps*LoadGraph.degree(nb) and (nb not in Queue):
                        Queue.append(nb)
                        #print('Adding node: ' + str(Queue))
        # when going through with the whole queue is done, check with 
        #r value of nodes in the queue. If smaller than threshold, remove it. 
        for node in Queue:
            if r[node] < eps*LoadGraph.degree(node):
                Queue.remove(node)
                #print('Removing node: ' + str(Queue))
        #print('Queue of current round: ' + str(Queue))
        
        #check those nodes whose r values are non zero
        tr = []
        for x in r:
            if r[x] > 0:
                tr.append(x) 
        #print('r of current round: ' + str(r))
        
    for item in ppr:
        if ppr[item] > 0:
            finalResult.append(item)
    return finalResult

#push operation. 
def Push(ppr, r, v, alpha, LoadGraph):
    pprtemp = ppr
    rtemp = r  
    pprtemp[v] = ppr[v] + alpha*r[v]
    rtemp[v] = ((1-alpha)/2)*r[v]
    for u in LoadGraph.neighbors(v):
        rtemp[u] = rtemp[u] + ((1-alpha)*rtemp[v])/(2*LoadGraph.degree(v)) 
    return pprtemp, rtemp
