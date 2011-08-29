from ssga import SSGA
import numpy

def fitness_sphere(sol):
    """ 
    Given an individual, it applied the sphere function
    >>> dim=10
    >>> import numpy
    >>> fitness_sphere(numpy.zeros(dim))
    0.0
    >>> fitness_sphere(numpy.arange(5))
    30
    """
    return (sol**2).sum()

def main():
    """
    Main program
    """
    domain = [-5, 5]
    dim=10
    ea = SSGA(domain=domain, size=60, dim=dim, fitness=fitness_sphere)
    ea.run(maxeval=dim*10000)
    [bestsol, bestfit] = ea.getBest()
    print "Best: %e\n" %bestfit
def test():
    import doctest
    doctest.testmod()
 
if __name__ == "__main__":
#    import psyco
#    psyco.log()
#    psyco.profile(0.2)
    main()
