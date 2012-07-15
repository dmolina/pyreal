from lettuce import *
import numpy as np
from numpy import random
from mock import patch, Mock
from localsearch import SolisWets 
import aspects
import utils

world.numevals = 0

def fun_fitness(sol):
    world.numevals += 1
    return (sol**2).sum()

domain = [-5, 5]
dim = 10


@step('I have an (.*) algorithm')
def have_sw(step,name):
    world.fitness_alias = []

    if name == 'SW':
	world.ls = SolisWets(fun_fitness, domain, dim)
    else:
	raise NameError('%s is unknown' %name)

@step('I have a random solution with dimension (\d+)')
def have_random_sol(step,dim):
    range = domain[1]-domain[0]
    world.sol = random.rand(int(dim))*range+domain[0]
    world.fitness = fun_fitness(world.sol)

@step('I have the optimum solution with dimension (\d+)')
def have_random_sol(step,dim):
    world.sol = np.zeros(int(dim))
    world.fitness = fun_fitness(world.sol)


@step('I improve with maxevals (\d+) and step size ([\d.]+)')
def improve_solution(step,maxevals,step_size):
    maxevals = int(maxevals)
    step_size = float(step_size)
    world.numevals = 0
    options = world.ls.getInitParameters(step_size)
    newsol = world.sol
    newfitness = world.fitness
    world.newsol, world.newfitness = world.ls.improve(newsol,newfitness,maxevals, options)

def assert_final_fitness(name,fitness,comparator):
    result = True

    if ('better' in comparator):
	result = world.newfitness < fitness
    elif ('worst' in comparator):
	result = world.newfitness > fitness
    elif ('equals' in comparator):
	result = world.newfitness == fitness

    if (comparator.startswith('not ')):
	result = not result

    assert result, "The final fitness is not %s than %s fitness" %(comparator,name)


@step('the final fitness should be (\w+) than previous one')
def comparison_fitness(steps,comparator):
    return assert_final_fitness('previous one', world.fitness, comparator)

@step('the final fitness should be (\w+) than (.+)')
def comparison_fitness(steps,comparator,name):
    assert world.fitness_alias[name] is not None
    fitness = world.fitness_alias[name]
    return assert_final_fitness(name, fitness, comparator)

@step('numevals is (\d+)')
def check_numevals(steps,numevals):
    numevals = int(numevals)
    assert world.numevals == numevals, "The numevals %d is not right, not equals to %d" %(world.numevals, numevals)

@step('Initial parameters with step size (\d+)')
def save_options(steps,step_size):
    world.init_options = world.ls.getInitParameters(step_size)
    world.options = world.init_options

@step('I load the initial parameters')
def load_options(steps):
    world.options = world.init_options
    world.fitness = []

@step('I improve with current parameters (\d+) times with maxevals (\d+)')
def improve_current_options(steps, num_times, max_evals, reference):
    newsol = world.sol
    newfitness = world.fitness
    options = world.options

    for i in range(num_times):
	newsol, newfitness = world.ls.improve(newsol,newfitness, max_evals, options)
    
    world.newsol = newsol
    world.newfitness = newfitness

@step('I save final fitness as (.+)')
def save_fitness(step,name):
    world.fitness_alias[name] = world.newfitness

@step('I save random generator')
def save_random(step):

