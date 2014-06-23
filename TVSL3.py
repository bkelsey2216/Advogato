import numpy as np
import random as rd

# simple method to combine two opinions A and B, both vectors of (b, d, n, e)
# following the combining operation in the paper
def comb(A,B):
    # the [1, 1, 1, 1] values don't mean anything yet; they are just placeholders
    # to specify the array dimensions. they get recalculated later based on the
    # combining equations
    result = np.array([1,1,1,1], dtype=float)
    b1=A[0]
    d1=A[1]
    u1=A[2]
    a1=A[3]
    b2=B[0]
    d2=B[1]
    u2=B[2]
    a2=B[3]
    result[0]=(b1*a2+b2*a1)/(a1+a2-a1*a2)     # recalculate b
    result[1]=(d1*a2+d2*a1)/(a1+a2-a1*a2)     # recalculate d
    result[2]=(u1*a2+u2*a1)/(a1+a2-a1*a2)     # recalculate n
    result[3]= a1*a2/(a1+a2-a1*a2)            # recalculate e
    return result

# simple method to discount two opinions A and B, both vectors of (b, d, n, e)
# following the discounting operation in the paper
def disc(A,B):
    result = np.array([1,1,1,1], dtype=float)
    b1=A[0]
    d1=A[1]
    u1=A[2]
    a1=A[3]
    b2=B[0]
    d2=B[1]
    u2=B[2]
    a2=B[3]
    result[0]=b1*b2
    result[1]=b1*d2
    result[2]=1-result[0]-result[1]-B[3]
    result[3]=B[3]
    return result

def TVSLTran(trust):     #transfer edge attribute to opinion

        rate = 0
        while rate <= 0 or rate >=10:   
        #*********
        #rate is used to control the ratio between b+d and e, or u (posterior) are set as 0.
        #********* 
            # rd.gauss creates a normal distribution/probablility density centered about
            # 1 (median/mean = 1) with a sigma squared of 0.25 (sigma/standard deviation = 0.5). 
            # This means that on average, the rate is 0.5 away from the mean.
            rate = 1
            #rate = rd.gauss(1, 0.25) # rate = 1 <--- true????

        result = np.array([1,1,1,1], dtype=float)

        # trust can be passed in as a string or float to calculate
        # the opinion vector

        if trust == 0.4  or trust == '"Observer"' or trust == 'Observer':
            # WHERE DO THESE CALCS COME FROM??? does it help them all stay controlled values < 1??:
            b = 0.4*(1 - 0.1*rate)
            d = 0.6*(1 - 0.1*rate)
            u = 0
            e = 0.1*rate
            result[0] = b
            result[1] = d
            result[2] = u
            result[3] = e
            return result
        elif trust == 0.6 or trust == '"Apprentice"' or trust == 'Apprentice':
            b = 0.6*(1 - 0.1*rate)
            d = 0.4*(1 - 0.1*rate)
            u = 0
            e = 0.1*rate
            result[0] = b
            result[1] = d
            result[2] = u
            result[3] = e
            return result
        elif (trust == 0.8) or (trust == '"Journeyer"') or trust == 'Journeyer': 
            b = 0.8*(1 - 0.1*rate)
            d = 0.2*(1 - 0.1*rate)
            u = 0
            e = 0.1*rate
            result[0] = b
            result[1] = d
            result[2] = u
            result[3] = e
            return result
        elif trust == 1 or trust == '"Master"' or trust == 'Master':
            b = 1*(1 - 0.1*rate)
            d = 0*(1 - 0.1*rate)
            u = 0
            e = 0.1*rate
            result[0] = b
            result[1] = d
            result[2] = u
            result[3] = e
            return result   

# Algorithm for assessing overall trust between two nodes, taking into account every path from the
# source to the destination that can be found on the graph. Combines/Discounts opininons as needed
# until only a one-hop direct path from src -> tgt exists, with an edge weight representing the 
# src's overall opinion of the tgt.
# PARAMETERS:
# G - the DiGraph of the population, edge weights representing trust levels
# src - source node
# tgt - destination node
# MaxHop - maximum path length (from src to tgt) TO IGNORE PATHS THAT ARE TOO LONG...?
# preHop - NOT SURE??? ITERATOR/HOP COUNT???
def TVSLAlgr(G, src, tgt, MaxHop, preHop):     #assess trust algr
    curHop = preHop + 1
    if curHop > MaxHop:    #check whether maxhop has been reached, if so, return numb
        #remove:
        print "negatives in curHop > MaxHop: " + src + " " + tgt
        return [-1, -1,-1,-1]   # how does this 
    
    nlist = G.neighbors(src)     #check the edges connected to current node
    if len(nlist) == 1:    #if there is only one edge, take it as original opinion and proceed forward. 
        preOpn =  TVSLTran(G[src][nlist[0]]['level'])
        if nlist[0] == tgt:  #if this opinion is directly connected to dst, return it
            #remove:
            print preOpn
            return preOpn
    
        else:
            posOpn = TVSLAlgr(G, nlist[0], tgt, MaxHop, curHop)   # if not, recursively recall TVSLAlgr and  take the resulting opinion as discounting opinion
            if posOpn[0] == -1:   #if the obtained opinion is invalid
                #remove:
                print "negatives: " + nlist[0] + " " + tgt
                return [-1, -1,-1,-1]
            else:
                #remove:
                print disc(posOpn, preOpn)  
                return  disc(posOpn, preOpn)  #else, discount it with previous opinion
    elif len(nlist) > 1:   #if more than 1 edges are connected to current node
        preOpnM = np.empty([len(nlist),4])   #matrix used to store opinions which are about to be combined
        for i, n in enumerate(nlist):    #for every connected edge
            preOpn =  TVSLTran(G[src][n]['level'])
            if n == tgt:
                preOpnM[i,:] = preOpn  #if it directly connected to dst, store it in the matrix. 
            else:
                posOpn = TVSLAlgr(G, n, tgt, MaxHop, curHop)  # if not, recursively recall TVSLAlgr and  put the resulting opinion into matrix
                if posOpn[0] == -1:
                    preOpnM[i,:] = [-1, -1,-1,-1]
                else:  
                    preOpnM[i,:] = disc(posOpn, preOpn)     #discount original opinion with discounting opinion, put resulting opinion into the matrix. 
                
        m = 0
        while preOpnM[i,:0] < 0:  #combing them together, but ignore invalid opinions
            m = m + 1
        sumOpn = preOpnM[m,:]
        for j, k in enumerate(nlist):
            if (j > m) and (preOpnM[j, 0] > 0):
                sumOpn = comb(sumOpn, preOpnM[j,:])
        #remove:
        print sumOpn
        return sumOpn
    else:
        #remove:
        print "negatives: " + nlist[0] + " " + tgt
        return [-1,-1,-1,-1]
    
# Method for calculating the expected belief of an opinion, given opinion vector A.
# total uncertainty = n + e = A[2] + A[3]
# and as defined in the paper, the expected belief of an opinion is computed
# using E = [[belief + bias*uncertainty]], where bias is set to 0.5 to represent an
# average amount of pre-existing stereotyping/bias    
def TVSLExp(A):
    return A[0] + 0.5*(A[2] + A[3])   #calculating the expected belief