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

@step('I have an SW algorithm')
def have_sw(step):
    world.ls = SolisWets(fun_fitness, domain, dim)

@step('I have a random solution with dimension (\d+)')
def have_random_sol(step,dim):
    range = domain[1]-domain[0]
    world.sol = random.rand(int(dim))*range+domain[0]
    world.fitness = fun_fitness(world.sol)

@step('I improve with maxevals (\d+) and step size ([\d.]+)')
def improve_solution(step,maxevals,step_size):
    maxevals = int(maxevals)
    step_size = float(step_size)
    world.numevals = 0
    options = world.ls.getInitParameters(step_size)
    newsol = world.sol
    newfitness = world.fitness
    world.ls.improve(newsol,newfitness,maxevals, options)
    world.newsol = newsol
    world.newfitness = newfitness

@step('the final fitness should be (\w+) than previous one')
def comparison_fitness(steps,comparator):
    result = True

    if ('better' in comparator):
	result = world.newfitness < world.fitness
    elif ('worst' in comparator):
	result = world.newfitness > world.fitness
    elif ('equals' in comparator):
	result = world.newfitness == world.fitness

    if (comparator.startswith('not ')):
	result = not result

    assert result, "The final fitness is not " +comparator +" than original fitness"

@step('numevals is (\d+)')
def check_numevals(steps,numevals):
    numevals = int(numevals)
    assert world.numevals == numevals, "The numevals %d is not right, not equals to %d" %(world.numevals, numevals)
