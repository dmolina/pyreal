import numpy as np
from numpy import array
import earandom as random
#import pyximport; pyximport.install(); import cutils
from cutils import getParentByNAM,crossBLX,applyMutationBGA,getBestWorst

class SSGA:
    """
    This class represent the Steady-State Genetic Algorithm
    using the BLX-0.5 crossover operator and BGA mutation to 12,5% genes
    """
    def __init__(self,fitness,domain,dim,size=60):
	"""
	Constructor

	fitness -- function fitness
	domain -- domain search (array with the lower and high values)
	dim -- integer with the dimensionality
	size -- popsize
	"""
	self.fitness = fitness
	self.domain = domain
	self.popsize = size
	self.dim=dim
	self.values = array([])
	self.fit_values = array([])
	self.set_mutation_rate(0.125)

    def set_mutation_rate(self,value):
	"""
	Sets a new mutation rate (% of mutation for individual)
	"""
	self.mutation_rate =value 
	self.mutationBGA_diff = [] 

    def population(self):
	""""
	Returns population (a copy)
	"""
	return self.values[:]


    def mutation(self, sol):
	"""
	Applies a mutation to the solution 
	sol -- solution to be muted (if it is required)
	"""
        def mutationBGA(value):
	    pieces=16
    
	    if len(self.mutationBGA_diff)==0:
		self.mutationBGA_diff = np.ones(pieces)/(2**np.arange(pieces))

	    return value+(random.randbool(pieces)*self.mutationBGA_diff).sum()
	    # TODO: Fixme
	    #return value+applyMutationBGA(random.randbool(pieces), self.mutationBGA_diff)
        
	newsol = sol

	if (self.mutation_rate > 0):

	    if  (random.rand()<=self.mutation_rate):
		newsol = np.copy(sol)
		pos = random.randint(0, self.dim-1)
		newsol[pos] = mutationBGA(newsol[pos])
            
	return newsol
    
    def population_fitness(self):
	"""
	Returns the fitness of each solution
	"""
	return self.fit_values

    def initPopulation(self,popsize):
	"""
	Init population (if it was assigned)
	"""
	self.popsize=popsize
	total = self.dim*self.popsize
	[low,high]=self.domain
	# Init the population
	totalvalues = random.randreal(low,high, total)
	self.values = np.resize(totalvalues,(self.popsize,self.dim))
	self.fit_values = array([self.fitness(sol) for sol in self.values])

    def updateWorst(self):
	[self.best,self.worst] = getBestWorst(self.fit_values)
	self.best_fitness = self.fit_values[self.best]
	self.worst_fitness = self.fit_values[self.worst]

    def updateBest(self):
	self.updateWorst()

    def getParents(self,tsize=3):
	"""
	Get the parents using the NAM selection 
	Mother is randomly selected.
	Parent is selected by competition between tsize random individuals (the individual which best/lower fitness is selected)

	Return [mother,parents] the position of individual to be crossed
	"""
	motherId = np.random.randint(self.popsize, size=1)[0]
	parentId = getParentByNAM(motherId,self.values, self.popsize, tsize)
	return [motherId,parentId]

    def cross(self,mother,parent,alpha=0.5):
	return crossBLX(mother,parent,self.domain,alpha)

    def crossSlow(self,mother,parent,alpha=0.5):
	diff = abs(mother-parent)
	I=diff*alpha
	points = np.array([mother,parent])
	vmin = np.vectorize(np.min)
	vmax = np.vectorize(np.max)
	A=vmin(mother,parent)-I
	B=vmax(mother,parent)+I
	children = random.uniform(A,B,self.dim)
	[low,high]=self.domain
	return np.clip(children, low, high)

    def reset(self):
	self.values=np.array([])

    def run(self,maxeval):
	self.maxeval=maxeval

	# Init the population
	if self.values.size ==0:
	    self.initPopulation(self.popsize)
	    numevals = self.popsize
	else:
	    numevals = 0

	# While numevals is not enough
	while numevals < maxeval:
	    [motherId,parentId] = self.getParents()
	    mother = self.values[motherId]
            parent = self.values[parentId]
	    # Crossover
	    children = self.cross(mother,parent)
	    # Mutation
	    children = self.mutation(children)
            fit_children = self.fitness(children) 
            numevals += 1
            self.updateWorst()

	    if fit_children < self.worst_fitness:
	        self.values[self.worst] = children
                self.fit_values[self.worst] = fit_children
             #   if (numevals % 50)==0:
             #       print "%d: %f" %(numevals,  fit_children)
                self.updateWorst()

	return numevals

    def getBest(self):
        best_sol = self.values[self.best]
        best_fitness = self.fit_values[self.best]
	return [best_sol, best_fitness]
