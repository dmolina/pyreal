import numpy as np
import math

def distance(ind1,ind2):
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
    dif = ind1-ind2
    sum = (dif*dif).sum()
    return math.sqrt(sum)

def distances(ind1,ind2):
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
    dif = ind1-ind2
    sum = (dif*dif).sum(axis=1)
    return np.sqrt(sum)


def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()

