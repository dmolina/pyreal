from lettuce import *
import numpy as np
from numpy import random
from mock import patch, Mock
from ssga import SSGA
import aspects
import utils

world.numevals = 0

def fitness(sol):
    world.numevals += 1
    return (sol**2).sum()

domain = [-5, 5]
popsize = 50
dim = 10

@step('I have a SSGA algorithm')
def have_configuration(step):
    world.ssga = SSGA(fitness,domain,dim,size=popsize)

@step('I have a SSGA algorithm for dimension (\d+)')
def have_configuration(step,dim):
    dim = int(dim)
    world.ssga = SSGA(fitness,domain,dim,size=popsize)


@step('I init the population with (\d+) individuals')
def init_population(step,popsize):
    world.popsize = int(popsize)
    world.ssga.initPopulation(int(popsize))

@step('population size is (\d+)')
def popsize_right(step,popsize_expected):
    popsize_expected = int(popsize_expected)
    (values_size,values_dim)=world.ssga.population().shape
    assert values_size == popsize_expected, "Got %d instead of %d" %(values_size,popsize_expected)
#    assert values_size == world.popsize, "Got %d" %values_size

@step('dimension for each individual is (\d+)')
def popsize_right(step,dim):
    dim = int(dim)
    population = world.ssga.population()
    (values_size,values_dim)=population.shape
    itera = 0
    
    for ind in population:
	assert ind.size == dim, "Individual %d has %d size" %(itera,ind.size) 
	itera += 1

@step('fitness is initialized')
def fitness_right(step):
    fits = world.ssga.population_fitness()
    assert fits.size == world.popsize, "Fitness size is zero"

@step('all fitness values are different')
def fitness_not_same(step):
    fits = world.ssga.population_fitness()
    assert np.unique(fits).size == world.popsize, "Fitness values are equals"

@step('I select parents with tournament size (\d+)')
def set_parents(step,tsize):
    world.nam_tsize=int(tsize)

@step('the parents are different after (\d+) tests')
def mother_parent_different(step,tests):
    tests = int(tests)

    for i in range(tests):
	[mother,parent]=world.ssga.getParents(world.nam_tsize)
	assert mother != parent, "Are the same individual"

@step('the distance between the parents is positive after (\d+) tests')
def best_parent(step):
    [motherId,parentId]=world.ssga.getParents(world.nam_tsize)
    population = world.ssga.population()


@step('the distance between parents is the longest')
def best_parent(step):
    ssga = world.ssga
    [motherId,parentId]=ssga.getParents(world.nam_tsize)
    population = ssga.population()
    mother = population[motherId]
    parent = population[parentId]
    distances = [utils.distance(population[i],mother) for i in range(world.popsize)]
    max_distances = np.array(distances).max()
    distance = utils.distance(parent, mother)
    assert distance == max_distances, "Distance from parent %f is different than maximum %f" %(distance, max_distances)

@step('I cross with alpha ([\d.]+)')
def apply_cross(self,alpha):
    alpha = float(alpha)
    world.children = world.ssga.cross(world.mother,world.parent,alpha)

@step('I set the same parent as mother')
def cross_same(self):
    population = world.ssga.population()
    motherId = random.randint(0, world.ssga.popsize)
    world.mother = population[motherId]
    world.parent = world.mother

@step('I set randomly two parents')
def cross_set_random(step):
    population = world.ssga.population()
    [motherId,parentId] = random.randint(0, world.ssga.popsize, 2)
    world.mother = population[motherId]
    world.parent= population[parentId]


@step('The children is the same')
def has_same_children(self):
    assert utils.distance(world.children, world.parent)==0, "Son distintos"

@step(u'When I use pseudorandoms=([\d.]+)')
def when_i_use_in_crossover_pseudorandoms_0(step, expected_random):
    world.patchRandom = patch('earandom.randreal', spec=True)
    world.random = world.patchRandom.start()
    expected_random = float(expected_random)
    world.random.return_value = expected_random*np.ones(dim)
#    world.patchRandom.stop()

@before.all
def init_random():
    world.patchRandom = None

def finish_random(rand):
    world.patchRandom.stop()

@step('The children is equals to the (\w+) of its parents')
def children_equals(self,strother):
    if (strother == 'minimum'):
	other = np.amin([world.mother, world.parent], axis=0)
    elif (strother == 'maximum'):
	other = np.amax([world.mother, world.parent], axis=0)
    elif (strother == 'mean'):
	other = 0.5*(world.mother+world.parent)
    else:
	assert False, "Error, criterion '%s' is not known" %strother
 
#    print world.mother
#    print world.parent
#    print world.children
#    print "\n"
    assert (world.children == other).all(), "Children is not equals to the '%s' of its parents" %strother
    finish_random(world.patchRandom)

@step('The children is between them')
def is_between_then(self):
    parents = np.array([world.mother,world.parent])
    min_parent = np.amin(parents,axis=0)
    max_parent = np.amax(parents,axis=0)
#    print world.mother
#    print world.parent
#    print world.children
#    print "\n"
    assert (world.children >= min_parent).all(), "Brokes inferior limit"
    assert (world.children <= max_parent).all(), "Brokes superior limit"

world.fitEval=[]
world.get_fitness = None

def measureFitness(*args, **kwargs):
    if world.fitEval == []:
	world.fitEval.append(world.get_fitness(world.ssga.population_fitness()))

    yield aspects.proceed
    world.fitEval.append(world.get_fitness(world.ssga.population_fitness()))
    
@step('I study the evolution of the (\w+) individual')
def study_population(self, individual):

    if individual == 'best':
	world.get_fitness = np.min
    elif individual == 'worst':
	world.get_fitness = np.max
    elif individual == 'mean':
	world.get_fitness = np.mean 
    else:
	assert False, "Error, individual '%s' is not known" %individual

    world.wrap_id = aspects.with_wrap(measureFitness, SSGA.updateWorst)

@step('I run the algorithm during (\d+) iterations')
def run_iterations(self,numevals):
    numevals = int(numevals)
    world.fitEval = []
    world.numevals = 0
    world.ssga.run(maxeval=numevals)

@step('they were evaluated (\d+) solutions')
def check_eval(self,solutions):
    assert world.numevals == int(solutions), "There wwere expected %d and not %s evaluations" %(world.numevals, solutions)

@step('its fitness is always better')
def check_fitness(self):
    size = len(world.fitEval)
    fitEval = world.fitEval
#    i = 0
#    for fit in fitEval:
#	i += 1
#	print "%d: %s" %(i,fit)

    for eval in xrange(size-1):
	before = float(fitEval[eval])
	after = float(fitEval[eval+1])
	assert after <= before, "In iteration %d fitness %f is lower than %f" %(eval,after, before)
    aspects.without_wrap(measureFitness, world.ssga.updateWorst)

@step('I set the mutation rate to (.+)')
def set_mutation_rate(step, mutation_rate):
    mutation_rate = float(mutation_rate)
    world.ssga.set_mutation_rate(mutation_rate)
    assert world.ssga.mutation_rate == mutation_rate

@step('I apply the mutation to (\d+) individuals')
def apply_mutation_to(step,number):
    num = int(number)
    world.inds_before_mutation = []
    world.inds_after_mutation = []

    for i in xrange(num):
	sol = random.rand(dim)
	world.inds_before_mutation.append(sol)
	world.inds_after_mutation.append(world.ssga.mutation(sol))
#	print sol
#	print world.ssga.mutation(sol)
	assert len(world.inds_after_mutation)==len(world.inds_before_mutation), "Mutation does not return individuals"

@step('about (\d+) individuals have been modified with range error (.+)')
def check_mutated(step,expected_changed,ratio):
    num = len(world.inds_before_mutation)
    expected = int(expected_changed)
    ratio = float(ratio)
    num_changed = 0

    for i in xrange(num):
	is_equals = (world.inds_before_mutation[i] == world.inds_after_mutation[i]).all()

	if not is_equals:
	    num_changed += 1

    assert abs(num_changed-expected)<=ratio, "Solution mutated are too different: %d expected and %d received" %(expected,num_changed)

@step('the mutated individuals differ only in 1 gen')
def check_change_1_gen(step):
    num = len(world.inds_before_mutation)

    for i in xrange(num):
	differ = (world.inds_before_mutation[i] != world.inds_after_mutation[i]).sum()
	assert differ == 1, "Error: Differ in %d gens" %differ
