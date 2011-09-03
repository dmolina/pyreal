from ssga import SSGA
from readargs import ArgsCEC05
import libpycec2005 as cec2005
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

def check_dimension(option, opt, value):
    if value not in [2, 10, 30, 50]:
        raise OptionValueError(
            "option %s: invalid dimensionality value: %r" % (opt, value))

def main():
    """
    Main program
    """
    args = ArgsCEC05()

    if  args.hasError:
	args.print_help_exit()

    fun = args.function
    dim = args.dimension

    print "Function: %d" %fun
    print "Dimension: %d" %dim
    cec2005.config(fun, dim)
    domain = cec2005.domain(fun)
#    domain = [-5, 5]
    print "Domain: ", domain
#    dim=10
    ea = SSGA(domain=domain, size=60, dim=dim, fitness=cec2005.evaluate)

    for x in xrange(25):
        ea.run(maxeval=dim*10000)
        [bestsol, bestfit] = ea.getBest()
        print "BestSol: ", bestsol
        print "BestFitness: %e" %bestfit
	ea.reset()

def test():
    import doctest
    doctest.testmod()
 
if __name__ == "__main__":
#    import psyco
#    psyco.log()
#    psyco.profile(0.2)
    main()
