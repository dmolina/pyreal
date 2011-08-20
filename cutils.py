#cython: boundscheck=False
#cython: wraparound=False
import numpy as np
from numpy import random
import math
from scipy import weave
import earandom as random

#def distance(np.array[double,ndim=1] ind1, np.array[double,ndim=1] ind2):
#    """
#    Euclidean distance
#    ind1 -- first array to compare
#    ind2 -- second array to compare
#   
#    Return euclidean distance between the individuals
#
#    >>> from numpy.random import rand
#    >>> import numpy as np
#    >>> dim = 30
#    >>> sol = rand(dim)
#    >>> distance(sol,sol)
#    0.0
#    >>> ref=np.zeros(dim)
#    >>> dist=distance(sol,ref)
#    >>> dist > 0
#    True
#    >>> dist2 = distance(sol*2,ref)
#    >>> 2*dist == dist2
#    True
#    """
#    cdef double suma
#    cdef double value
#    cdef unsigned int size
#
#    size = ind1.shape[0]
#    suma = 0
#
#    for i in xrange(1,size):
#	value =  (ind1[i]-ind2[i])
#	suma += value*value
#
#    return math.sqrt(suma)

def getRemoteVector(vectors, reference):
    """
    Get the more remote parents

    Parents -- Matrix with the different individual to compare
    Mother -- Reference individual

    Returns index of the most remote individual 
    """
    code = """
    #line 52 "cutils.py"
    int i, j;
    double max;
    double dist, value, maxdist;
    maxdist = -1;

    for (i = 0; i < Nu[0]; i++) {
	dist = 0;

	for (j = 0; j < Nu[1]; j++) {
	    value = U2(i, j) - V1(j);
	    dist += value*value;
	}
	dist = sqrt(dist);

	if (dist > maxdist || maxdist < 0) {
	    maxdist = dist;
	    BEST1(0) = i;
	}
    }
    """
    best = np.array([1])
    u = vectors
    v = reference
    weave.inline(code, ['u', 'v', 'best'])
    return best


def getFromPermutation(max, num):
    """
    Returns elements of a permutation, because random.permutation is too low

    size -- size to elements
    num  -- numbers to select 
    """
    code = """
	#line 85 "cutils.py"
	int *arange = (int *) malloc(sizeof(int)*max);
	int i, value;

	for (i = 0; i < max; i++) {
	    arange[i] = i;
	}

	for (i = 0; i < num; i++) {
	    value = int(RAND1(i) % (num-i+1));
	    RESULTS1(i) = arange[value];
	    arange[value] = arange[num-i-1];
	}
	
	free(arange);
    """
    assert num <= max
    rand = random.randreal(0, max, size=num)
    results = np.array(np.zeros(num,dtype=np.int8))
    weave.inline(code, ['rand','max','num','results'])
    return results

def crossBLX(mother,parent,domain,alpha):
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
    >>> sol = np.array([1,2,3,2,1])
    >>> crossBLX(sol,sol,[low,upper],0)
    array([ 1.,  2.,  3.,  2.,  1.])
    """
    code = """
    #line 128 "cutils.py"
    double diff,I,A,B;
    double x, y;
    int i;

    for (i = 0; i < Nm[0]; i++) {
	
	if (M1(i) < P1(i) ) {
	    x = M1(i);
	    y = P1(i);
	}
	else {
	    y = M1(i);
	    x = P1(i);
	}

	I = alpha*(y-x);
	A = x-I;
	B = y+I;

	if (A < lower)
	    A = lower;
	if (B > upper)
	    B = upper;

	C1(i) = A+R1(i)*(B-A);
    }
    """
    dim = mother.size
    m = mother
    p = parent
    r = random.randreal(0,1,dim)
    c = np.array(np.zeros(dim))
    [lower,upper]=domain
    weave.inline(code, ["m","p","r","alpha","lower","upper","c"])
    return c

def getParentByNAM(motherId,values,popsize,tsize=3):
    """
    Get the parent using the NAM selection 
    Parent is selected by competition between tsize random individuals (the individual which best/lower fitness is selected)
    
    Return the parent more distant from motherId
    """

    code = """
    #line 178 "cutils.py"
    int *arange = (int *) malloc(sizeof(int)*max);
    int *parents = (int *) malloc(sizeof(int)*num);
    int i, j, posi, limit,dim;
    int reference = (int) ref;
    double dist, value, maxdist;
    maxdist = -1;

    // Init the permutation
    for (i = 0; i < max; i++) {
	arange[i] = i;
    }
    arange[reference] = arange[max-1];
    max-=1;

    // Get the random individuals
    for (i = 0; i < num; i++) {
	limit = (max-i-1);
	posi = (int) rint(RAND1(i)*limit);
	parents[i] = arange[posi];
	arange[posi] = arange[limit];
    }
	
    free(arange);
    dim = Nd[1];

    // Obtains the most distant parents
    for (i = 0; i < num; i++) {
	posi = parents[i];
	dist = 0;

	for (j = 0; j < dim; j++) {
	    value = D2(posi, j) - D2(reference, j);
	    dist += value*value;
	}
	dist = sqrt(dist);

	if (dist > maxdist || maxdist < 0) {
	    maxdist = dist;
	    BEST1(0) = posi;
	}
    }
    free(parents);
    """
    rand = random.randreal(0.0, 1.0, tsize)
    max = popsize
    num = tsize
    d = values
    (psize,dim)=values.shape
    ref = motherId
    best = np.array([0])
    weave.inline(code, ['ref','rand','max','num','d','best'])
    return best[0]

def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()

