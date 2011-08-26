from __future__ import division
from ssga import SSGA
import numpy as np
import matplotlib
matplotlib.use('GTKAgg') # do this before importing pylab
import matplotlib.pyplot as plt
from pylab import *
import aspects

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

def plot_func():


    def func3(x,y):
	    return (1- x/2 + x**5 + y**3)*exp(-x**2-y**2)

    # make these smaller to increase the resolution
    dx, dy = 0.05, 0.05

    x = arange(-3.0, 3.0, dx)
    y = arange(-3.0, 3.0, dy)
    X,Y = meshgrid(x, y)
    
    Z = func3(X, Y)
    
    ax = subplot(111)
    im = imshow(Z, cmap=cm.jet)
    #im.set_interpolation('nearest')
    #im.set_interpolation('bicubic')
    im.set_interpolation('bilinear')
    #ax.set_image_extent(-3, 3, -3, 3)

    show()

def plot_static(minimum, maximum, dif):
    def sphere_two(x,y):
	return (x**2+y**2)

    dx = dy = dif
    x = arange(minimum, maximum, dx)
    y = arange(minimum, maximum, dy)
    X,Y = meshgrid(x, y)
    Z = sphere_two(X, Y)
    fig = plt.figure()
    ax = subplot(111)
    x, y = (np.random.rand(2, 50))*100
    ax.plot(x, y, 'wo')
    im = imshow(Z, cmap=cm.jet)
    im.set_interpolation('bilinear')
    show()

line = None
population = None
ax = None

def measureFitness(*args, **kwargs):
    yield aspects.proceed
    x = population[:,0]
    y = population[:,1]
    line.set_xdata(x)
    line.set_ydata(y)
    fig.canvas.draw()

def plot_anim_ssga(minimum, maximum, dif):
    def sphere_two(x,y):
	return (x**2+y**2)

    dx = dy = dif
    x = arange(minimum, maximum, dx)
    y = arange(minimum, maximum, dy)
    X,Y = meshgrid(x, y)
    Z = sphere_two(X, Y)
    fig = plt.figure()
    ax = subplot(111)
    x, y = (np.random.rand(2, 50))*100
    #ax.plot(x, y, 'wo')
    im = imshow(Z, cmap=cm.jet)
    im.set_interpolation('bilinear')
    #show()

    domain = [-5, 5]
    dim=2
    ea = SSGA(domain=domain, size=50, dim=dim, fitness=fitness_sphere)
    ea.initPopulation(dim)
    population = ea.population()
    x = population[:,0]
    y = population[:,1]
    line, = ax.plot(x, y, 'wo')
    ea.run(maxeval=dim*10000)

    import gobject
    print 'adding idle'
    gobject.idle_add(animate)
    print 'showing'
    plt.show()

def plot_anim(minimum, maximum, dif):
    def sphere_two(x,y):
	return (x**2+y**2)

    def animate():
	x, y = (np.random.rand(2, 1))*50
        line, = ax.plot(x, y, 'wo')

	for i in np.arange(1,20000):
	    x, y = (np.random.rand(2, 50))*40
#	    line.set_xdata(x)
#	    line.set_ydata(y)
	    fig.canvas.draw()

	raise SystemExit

    dx = dy = dif
    x = arange(minimum, maximum, dx)
    y = arange(minimum, maximum, dy)
    X,Y = meshgrid(x, y)
    Z = sphere_two(X, Y)
    fig = plt.figure()
    ax = subplot(111)
    x, y = (np.random.rand(2, 50))*100
    #ax.plot(x, y, 'wo')
    im = imshow(Z, cmap=cm.jet)
    im.set_interpolation('bilinear')
    #show()

    import gobject
    print 'adding idle'
    gobject.idle_add(animate)
    print 'showing'
    plt.show()


def main():
    """
    Main program
    """
    domain = [-5, 5]
    dim=2
    ea = SSGA(domain=domain, size=60, dim=dim, fitness=fitness_sphere)
    ea.run(maxeval=dim*10000)
    [bestsol, bestfit] = ea.getBest()
    print "Best: %f\n" %bestfit
def test():
    import doctest
    doctest.testmod()
 
if __name__ == "__main__":
    plot_anim_ssga(-5, 5, 0.1)
