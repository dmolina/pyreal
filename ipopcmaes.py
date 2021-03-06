import cma
import logging
import math
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
    restevals = maxevals
    popsize = 4+int(3*math.log(dim))
    initial = np.random.rand(dim)*(max-min)+min

    print "===================================="
    print "Popsize: %d" %popsize

    while restevals > 0:
#    for lam in 10 * 2**np.arange(7):  # 10, 20, 40, 80, ..., 10 * 2**6
	initial = np.random.rand(dim)*(max-min)+min
	es = cma.CMAEvolutionStrategy(initial,
	(max-min)/2.0,         # initial std sigma0
	# bounds 
	{
	    'maxfevals': restevals, 
	    'CMA_active': 1,
#	     'verb_disp': 500,
#	     'tolfun': 1e-12,
	    'popsize': popsize, 'verb_append': bestever.evalsall, 'bounds': [min,max]})   # pass options
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
	#cma.pprint(bestever.x)
	#cma.pprint(bestever.f)
	#print "NumEvals: %d" %es.result()[3]

	if bestever.f < 1e-8:  # global optimum was hit
	    break
	else:
	    evals = es.result()[3]
	    restevals = restevals - evals
	    print "It rests %d evaluations" %restevals
	    popsize = 2*popsize
	    print "Popsize: %d" %popsize
	    print "-------------------------------"

    print "===================================="
    return (bestever.x,bestever.f)

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
