import cma
import logging
from readargs import ArgsCEC05
import libpycec2005 as cec2005
import numpy as np

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

def ipopcmaes(fitness_eval,domain,dim,maxevals):
    # restart with increasing population size (IPOP)
    bestever = cma.BestSolution()
    (min,max)=domain

    for lam in 10 * 2**np.arange(7):  # 10, 20, 40, 80, ..., 10 * 2**6
	es = cma.CMAEvolutionStrategy(np.random.rand(dim)*(max-min)+min,
	(max-min)/3.0,         # initial std sigma0
	# bounds 
	{'maxfevals': maxevals, 'tolfun': '1e-8', 
	    'popsize': lam, 'verb_append': bestever.evalsall, 'bounds': [min,max]})   # pass options
	#logger = logging.getLogger('ipopcmaes')

	while not es.stop():
	    X = es.ask()    # get list of new solutions
	    fit = [fitness_eval(x) for x in X]  # evaluate each solution
	    es.tell(X, fit) # besides for termination only the ranking in fit is used
	    # display some output
	    #logger.add()  # add a "data point" to the log, writing in files
	    es.disp()  # uses option verb_disp with default 100
	    #print('termination:', es.stop())
	    #cma.pprint(es.best.__dict__)
	    bestever.update(es.best)
	    # show a plot
	    #logger.plot()

	    if bestever.f < 1e-8:  # global optimum was hit
		break
	
	cma.pprint(es.result())
	return (es.result()[0],es.result()[1])
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

    for x in xrange(25):
	bestsol,bestfit = ipopcmaes(cec2005.evaluate,domain,dim,maxevals=dim*10000)
        print "BestSol: ", bestsol
        print "BestFitness: %e" %bestfit
	print "%e" %bestfit

def test():
    import doctest
    doctest.testmod()
 
if __name__ == "__main__":
#    import psyco
#    psyco.log()
#    psyco.profile(0.2)
    main()
