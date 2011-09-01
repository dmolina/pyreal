# cython: boundscheck=False
import math
import numpy as np
cimport numpy as np
cimport cython
import earandom as random
DTYPE = np.double
ctypedef np.double_t DTYPE_t
ctypedef np.int_t BTYPE_t

def distance(np.ndarray[DTYPE_t, ndim=1]ind1, np.ndarray[DTYPE_t, ndim=1] ind2):
    """
    Euclidean distance
    ind1 -- first array to compare
    ind2 -- second array to compare
   
    Return euclidean distance between the individuals

    >>> from numpy.random import rand
    >>> import numpy as np
    >>> dim = 30
    >>> sol = rand(dim)
    >>> distance(sol,sol)
    0.0
    >>> ref=np.zeros(dim)
    >>> dist=distance(sol,ref)
    >>> dist > 0
    True
    >>> dist2 = distance(sol*2,ref)
    >>> 2*dist == dist2
    True
    """
    cdef np.ndarray[DTYPE_t, ndim=1] dif = ind1-ind2
    cdef double sum = (dif*dif).sum()
    return math.sqrt(sum)

def distances(np.ndarray[DTYPE_t, ndim=1] ind1,np.ndarray[DTYPE_t, ndim=1] ind2):
    """
    Euclidean distance
    ind1 -- first array to compare
    ind2 -- second array to compare
   
    Return euclidean distance between the individuals

    >>> from numpy.random import rand
    >>> import numpy as np
    >>> dim = 30
    >>> sol = rand(dim)
    >>> distance(sol,sol)
    0.0
    >>> ref=np.zeros(dim)
    >>> dist=distance(sol,ref)
    >>> dist > 0
    True
    >>> dist2 = distance(sol*2,ref)
    >>> 2*dist == dist2
    True
    """
    cdef np.ndarray[DTYPE_t, ndim=1] dif = ind1-ind2
    cdef double sum = (dif*dif).sum(axis=1)
    return np.sqrt(sum)

def getRemoteVector(np.ndarray[DTYPE_t, ndim=2] vectors, np.ndarray[DTYPE_t, ndim=1] reference):
    """
    Get the more remote parents

    Parents -- Matrix with the different individual to compare
    Mother -- Reference individual

    Returns index of the most remote individual 
    """
    cdef int i, dim, size, bestpos
    cdef double value, dist, maxdist

    dim = vectors.shape[1]
    size = vectors.shape[0]
#    print "dim: %d\tsize: %d\n" %(dim,size)
    bestpos=0
    maxdist = -1

    for i in range(size):
        dist = 0

#        for j in range(dim):
#            value = vectors[i,j] - reference[j]
#            dist += value*value
#
#        dist = math.sqrt(dist)
#
#        if (dist > maxdist or maxdist < 0):
#           maxdist = dist
#           bestpos = i
	
	
    return bestpos

    #cdef np.ndarray[DTYPE_t, ndim=1] dif=(vectors-reference)
    #cdef np.ndarray[DTYPE_t, ndim=1] distances = np.sqrt((dif*dif).sum(axis=1))
    #return np.argmax(distances)

cdef list getFromPermutation(double reference, int max, int num):
    cdef np.ndarray values = np.random.permutation(max)
    cdef list values2 = [x for x in values if x != reference]
    return values2[0:(num+1)]

def crossBLX(np.ndarray[DTYPE_t, ndim=1] mother,np.ndarray[DTYPE_t, ndim=1] parent,list domain, double alpha):
    """
    crossover operator BLX-alpha
    
    mother -- mother (first individual)
    parent -- parent (second individual)
    domain -- domain to check
    alpha  -- parameter alpha

    Returns the new children following the expression children = random(x-alpha*dif, y+alpha*dif), 
		where dif=abs(x,y) and x=lower(mother,parents), y=upper(mother,parents) 

    >>> import numpy as np
    >>> low=-5
    >>> upper = 5
    >>> dim=30
    >>> sol = np.ndarray([1,2,3,2,1])
    >>> crossBLX(sol,sol,[low,upper],0)
    array([ 1.,  2.,  3.,  2.,  1.])
    """
    cdef np.ndarray[DTYPE_t, ndim=1] C, r
    cdef int low, high, dim
    cdef double x, y
    cdef double I, A, B
    cdef unsigned i
    [low,high]=domain
    dim = mother.shape[0]
    C = np.zeros(dim)
    r = random.randreal(0,1,dim)

    for i in range(dim):
        if mother[i] < parent[i]:
           (x,y) = (mother[i],parent[i])
        else:
           (y,x) = (mother[i],parent[i])

        I = alpha*(y-x)
        A=x-I
        B=y+I
        
        if (A < low):
            A = low
        if (B > high):
            B = high
        
        C[i] = A+r[i]*(B-A)
    
    return C

def getParentByNAM(int motherId,np.ndarray[DTYPE_t, ndim=2] pop, int popsize, int tsize=3):
    """
    Get the parent using the NAM selection 
    Parent is selected by competition between tsize random individuals (the individual which best/lower fitness is selected)
    
    Return the parent more distant from motherId
    """
    cdef np.ndarray[DTYPE_t,ndim=1] rand
    cdef np.ndarray[np.int_t,ndim=1] arange
    cdef int parent,max, ref
    cdef double value, dist, maxdist
    cdef int dim, parentId, limit
    cdef np.ndarray[DTYPE_t,ndim=1] ind, ind_ref
    cdef unsigned i, j, posi

    rand = random.randreal(0.0, 1.0, tsize)
    dim = pop.shape[1]
    ref = motherId
    max = popsize
    # Init the permutation
    arange = np.arange(0, max)
    arange[ref] = arange[max-1]
    max -= 1
    ind_ref = pop[ref]
    maxdist = -1

    # Get the random individuals
    for i in range(tsize):
        limit = (max-i-1)
        posi = round(rand[i]*limit)
        parent = arange[posi]
        arange[posi] = arange[limit]
        ind = pop[parent]
        dist = 0
        
        for j in range(dim):
            value = ind[j] - ind_ref[j]
            dist += value**2
        
        if dist > maxdist or maxdist < 0:
            maxdist = dist
            parentId = parent

    return parentId

def applyMutationBGA(np.ndarray[BTYPE_t, ndim=1] randbool, np.ndarray[DTYPE_t, ndim=2] mutationdiff):
    return (randbool*mutationdiff).sum()

def getBestWorst(np.ndarray[DTYPE_t, ndim=1] fitness):
    cdef unsigned best, worst
    cdef double fit, maxfit, minfit
    cdef unsigned i
    cdef unsigned size 

    size = fitness.shape[0]
    minfit = maxfit = fitness[0]
    best = worst = 0

    for i in range(size):
        fit = fitness[i]
        
        if fit < minfit:
            minfit = fit
            best = i
        elif fit > maxfit:
            maxfit = fit
            worst = i

    return [best,worst]

def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()

