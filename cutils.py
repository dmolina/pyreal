#cython: boundscheck=False
#cython: wraparound=False
import numpy as np
import math
from scipy import weave

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

    for (i = 0; i < NU[0]; i++) {
	dist = 0;

	for (j = 0; j < NU[1]; j++) {
	    value = U2(i, j) - V1(j);
	    dist += value*value;
	}

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
	    value = RAND1(i) % (num-i+1);
	    RESULTS1(i) = arange[value];
	    arange[value] = arange[num-i-1];
	}
	
	free(arange);
    """
    assert num <= max
    rand = np.random.randint(max, size=num)
    results = np.array(np.zeros(num,dtype=np.int8))
    weave.inline(code, ['rand','max','num','results'])
    return results

def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()

