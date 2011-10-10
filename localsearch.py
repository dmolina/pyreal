import numpy as np

#class CMAES:
#    """
#    This class implement the CMA-ES algorithm
#    """
#    def __init__(self,fitness,maxeval,domain):	
#	"""
#	Init the class. 
#
#	fitness -- Fitness function to improve
#	maxeval -- maximum evaluation number
#	domain  -- domain search (array with [min,max] values)
#	"""
#	self.fitness = fitness
#	self.maxeval = maxeval
#	self.domain  = domain
#

class LocalSearch:
    """
    This class implements the interfaz of each LS method
    """
    def __init__(self, fitness, domain, dim):
	"""
	Init the class. 

	fitness -- Fitness function to improve
	domain  -- domain search (array with [min,max] values)
	"""
	raise BaseException("Not defined LS::init")

    def getInitParameters(self, delta):
	""""
	Allow to returns a options hashkey with all the important parameters

	delta  -- initial step size of the search 

	return -- the hash key with all initial options
	"""
	raise BaseException("Not defined LS::getInitParameters")

    def improve(self, sol, fitness, maxeval, options):
	"""
	Apply the Local Search process

	sol     -- numarray with the solution to improve
	delta   -- range of the initial search
	fitness -- final fitness of the solution
	maxeval -- maximum evaluation number
	options -- options resulting of getInitParameters or previous 
	           improve operation
	"""
	raise BaseException("Not defined LS::improve")

class SolisWets(LocalSearch):
    """
    This class implement the Solis Wets implementation
    """
    maxSuccess = 5
    maxFailed = 3

    def __init__(self, fitness, domain, dim):
	"""
	Init the class. 

	fitness -- Fitness function to improve
	maxeval -- maximum evaluation number
	domain  -- domain search (array with [min,max] values)
	"""
	self.fitness = fitness
	self.domain  = domain
	self.dim = dim

    def getInitParameters(self, delta):
	options = {}
	options['delta']=delta
	options['successes'] = options['fails'] = 0
	options['bias'] = np.zeros(self.dim)
	return options

    def clip(self, sol):
	return np.clip(sol, self.domain[0], self.domain[1])

    def getNeighbour(self, actual, options):
	"""
	Generate the new solutions, using a distance vector and the inercia vector
	"""
	diff = np.random.normal(options['delta'])
	newsol = actual+options['bias']*diff
	newsol = self.clip(newsol)
	return (newsol,diff)

    def incremBias(self, dif, bias):
	"""
	Increm the bias
	"""
	return 0.2*bias + 0.4*(dif+bias)

    def reduceBias(self,dif, bias):
	"""
	Reduce the bias
	"""
	return bias - 0.4*(dif+bias)

    def divideBias(self, bias):
	return bias/2.0

    def improve(self,sol,fitness,maxeval,options):
	"""
	Apply the Local Search process

	sol   -- numarray with the solution to improve
	delta -- range of the initial search
	"""
	numEval = 0
	assert fitness > 0

	while (numEval < maxeval):
	    (newsol,diff) = self.getNeighbour(sol,options)
	    newfitness = self.fitness(newsol)
	    numEval += 1

	    if (newfitness < fitness):
		sol = newsol
		fitness = newfitness
		options['bias'] = self.incremBias(diff, options['bias'])
		options['successes'] += 1
		options['fails'] = 0
	    elif (numEval < maxeval):
		newsol = self.clip(sol-options['bias']-diff)
		newfitness = self.fitness(newsol)
		numEval += 1

		if (newfitness < fitness):
		    sol = newsol
		    fitness = newfitness
		    options['bias'] = self.reduceBias(diff, options['bias'])

		    options['successes'] += 1
		    options['fails'] = 0
		else:
		    options['bias'] = self.divideBias(options['bias'])
		    options['successes'] = 0
		    options['fails'] += 1

	    if (options['successes'] >= self.maxSuccess):
	       options['successes'] = 0
	       options['delta'] *= 2.0
	    elif (options['fails'] >= self.maxFailed):
	       options['fails'] = 0
	       options['delta'] /= 2.0

	return numEval
