def localPartitioningAttempt(alpha, beta):

# Offline Preprocessing:
# We must compute two global PageRank vectors.
# 1. Let gamma = alpha + beta − alpha beta.
	gamma = alpha + beta - alpha * beta
# 2. Let W = W(A) be the random walk matrix of A.
	W = calculateRandomWalkMatrix()
# 3. Compute the two global PageRank vectors prbeta = prW (beta, psy) and prgamma =
# prW (gamma, psy) using the algorithm GlobalPR.
	#psy means that nstart = none which means that there will be a normal distribution for the
	#starting vector which means that we are calculating global page rank
 	prBeta  = nx.pagerank(W, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='weight', dangling=None)
 	prGamma = nx.pagerank(W, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='weight', dangling=None)

# Local Computation:
# 1. Pick a starting vertex v.
	for node in DG.nodes(): ????????
# 2. Compute prW (gamma, v), using LocalPR.
	inputVector = []
	for i in range (0,len(DG.nodes)):
		startVector.append(0)
	startVector[node] = 1
	prPersonal = nx.pagerank(W, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=startVector, weight='weight', dangling=None)

# 3. Obtain p = prMbeta (alpha, v) by taking a linear combination of prW (gamma, v) and
# prW(gamma,psy),
# p = prMbeta (alpha, v) = alpha prW (gamma, v) + (1 − alpha)beta prW (gamma, psy).
	p = alpha * prPersonal + (1 - alpha) * beta * prGamma
# 4. Rank the vertices in nonincreasing order of p(x)/prbeta(x).
# 5. Let Sj be the set of the top j vertices in this ranking.

# 6. Compute the beta-conductances Φbeta (Sj ) for each set Sj , and output the set
# with the smallest beta-conductance.
	minConductanceIndex = 0
	minConductance = calculateConductance(sortedVector[0:1])
	for j in range(1:len(Sj)):
		if minConductance < calculateConductance(sortedVector[1:j]):
			minConductance = calculateConductance(sortedVector[1:j])
			minConductanceIndex = j
	return Sj[0:minConductanceIndex]



def localPartitioningAttempt(alpha, beta):
	A = nx.adjacency_matrix(DG)
	print(A.todense())
	A.setdiag(1)
	print(A.todense())
	W = calculateRandomWalkMatrix(A)

def calculateRandomWalkMatrix(A):
	D = kjfndsiuffiuhadf
	return (eye())




