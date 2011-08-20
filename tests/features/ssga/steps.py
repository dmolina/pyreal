from lettuce import *
import numpy as np
from numpy import random
from ssga import SSGA
import utils

def fitness(sol):
    return (sol**2).sum()

domain = [-5, 5]
popsize = 50
dim = 10

@step('I have a SSGA algorithm')
def have_configuration(step):
    world.ssga = SSGA(fitness,domain,dim,size=popsize)

@step('I init the population with (\d+)')
def init_population(step,popsize):
    world.popsize = int(popsize)
    world.ssga.initPopulation(int(popsize))

@step('popsize is right')
def popsize_right(step):
    (values_size,values_dim)=world.ssga.population().shape
    assert values_size == popsize, "Got %d" %values_size

@step('dimension for each individual is right')
def popsize_right(step):
    population = world.ssga.population()
    (values_size,values_dim)=population.shape
    itera = 0
    
    for ind in population:
	assert ind.size == dim, "Individual %d has %d size" %(itera,ind.size) 
	itera += 1

@step('fitness is initialized')
def fitness_right(step):
    fits = world.ssga.population_fitness()
    assert fits.size == popsize, "Fitness size is zero"

@step('all fitness values are different')
def fitness_not_same(step):
    fits = world.ssga.population_fitness()
    assert np.unique(fits).size == popsize, "Fitness values are equals"

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


@step('the parent or the mother is the furthest')
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


@step('I use uniform with values=(\d+)')
def set_uniform(step, values, mock_uniform):
    uniform.side_effect = get_values(lambda u, v, dim: u+(v-u)*v)

@step('The children is the same')
def has_same_children(self):
    assert utils.distance(world.children, world.parent)==0, "Son distintos"

@step(u'When I use in crossover pseudorandoms=0')
def when_i_use_in_crossover_pseudorandoms_0(step):
    assert False, 'This step must be implemented'

@step('The children is between them')
def is_between_then(self):
    parents = np.array([world.mother,world.parent])
    min_parent = np.amin(parents,axis=0)
    max_parent = np.amax(parents,axis=0)
    assert (world.children >= min_parent).all(), "Brokes inferior limit"
    assert (world.children <= max_parent).all(), "Brokes superior limit"
