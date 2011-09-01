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

def getRemoteVector(vectors,reference):
    """
    Get the more remote parents

    Parents -- Matrix with the different individual to compare
    Mother -- Reference individual

    Returns index of the most remote individual 
    """
    dif=(vectors-reference)
    distances = np.sqrt((dif*dif).sum(axis=1))
    return np.argmax(distances)

def getFromPermutation(reference, max, num):
    values = np.random.permutation(max)
    values2 = [x for x in values if x != reference]
    return values2[0:(num+1)]

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
    diff = abs(mother-parent)
    dim = mother.size
    I=diff*alpha
    points = np.array([mother,parent])
    A=np.amin(points,axis=0)-I
    B=np.amax(points,axis=0)+I
    children = np.random.uniform(A,B,dim)
    [low,high]=domain
    return np.clip(children, low, high)

def getParentByNAM(motherId,values,popsize,tsize=3):
    """
    Get the parent using the NAM selection 
    Parent is selected by competition between tsize random individuals (the individual which best/lower fitness is selected)
    
    Return the parent more distant from motherId
    """
    random = getFromPermutation(motherId, popsize, tsize+1)
    # parents 
    idParents = random[1:]
    mother = values[motherId]
    Parents = values[idParents]
    return idParents[getRemoteVector(Parents,mother)]

def applyMutationBGA(randbool, mutationdiff):
    return (randbool*mutationdiff).sum()

def getBestWorst(fitness):
    best = np.argmin(fitness)
    worst = np.argmax(fitness)
    return [best,worst]

def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()

