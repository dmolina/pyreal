#!/usr/bin/python
#
# Josh Lifton 2004
#
# Permission is hereby granted to use and abuse this document
# so long as proper attribution is given.
#
# This Python script demonstrates how to use the numarray package
# to generate and handle large arrays of data and how to use the
# matplotlib package to generate plots from the data and then save
# those plots as images.  These images are then stitched together
# by Mencoder to create a movie of the plotted data.  This script
# is for demonstration purposes only and is not intended to be
# for general use.  In particular, you will likely need to modify
# the script to suit your own needs.
#
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt   # For plotting graphs.
from pylab import *
import numpy as np
import subprocess                 # For issuing commands to the OS.
import os
import sys                        # For determining the Python version.
from ssga import SSGA
import aspects

#
# Print the version information for the machine, OS,
# Python interpreter, and matplotlib.  The version of
# Mencoder is printed when it is called.
#
print 'Executing on', os.uname()
print 'Python version', sys.version
print 'matplotlib version', matplotlib.__version__

not_found_msg = """
The mencoder command was not found;
mencoder is used by this script to make an avi file from a set of pngs.
It is typically not installed by default on linux distros because of
legal restrictions, but it is widely available.
"""

try:
    subprocess.check_call(['mencoder'])
except subprocess.CalledProcessError:
    print "mencoder command was found"
    pass # mencoder is found, but returns non-zero exit as expected
    # This is a quick and dirty check; it leaves some spurious output
    # for the user to puzzle over.
except OSError:
    print not_found_msg
    sys.exit("quitting\n")


#
# First, let's create some data to work with.  In this example
# we'll use a normalized Gaussian waveform whose mean and
# standard deviation both increase linearly with time.  Such a
# waveform can be thought of as a propagating system that loses
# coherence over time, as might happen to the probability
# distribution of a clock subjected to independent, identically
# distributed Gaussian noise at each time step.
#

print 'Initializing data set...'   # Let the user know what's happening.

eval = 0

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
    global eval
    eval += 1
    return np.sqrt(sol[0]**2+sol[1]**2)

def fitness_rosenbrock(sol):
    """ 
    Given an individual, it applied the sphere function
    >>> dim=10
    >>> import numpy
    >>> fitness_sphere(numpy.zeros(dim))
    0.0
    >>> fitness_sphere(numpy.arange(5))
    30
    """
    global eval
    eval += 1
    global dim
    F = 0.0

    for i in range(dim-1):
	F += 100*pow(pow(sol[i], 2)-sol[i+1], 2)+pow(sol[i]-1, 2)
    return F


# Initialize variables needed to create and store the example data set.
numberOfTimeSteps = 200   # Number of frames we want in the movie.
# Init the ssga
domain = [-5, 5]
dim=2
function_fitness = fitness_sphere
ea = SSGA(domain=domain, size=50, dim=dim, fitness=function_fitness)

# Create an array of zeros and fill it with the example data.
print 'Done.'                       # Let the user know what's happening.
frame=0
stepframe=5

def save():
    global eval
    global frame
    filename = str('population%03d' % frame) + '.png'
    frame += 1
    plt.savefig(filename, dpi=100)
    # Let the user know what's happening.
    print 'Wrote file', filename

line = None
fig = None

# Now that we have an example data set (x,y) to work with, we can
# start graphing it and saving the images.
def measureFitness(*args, **kwargs):
    yield aspects.proceed

    if ( (eval % stepframe)==1):
	population = ea.population()
	x = (population[:,0]+5)*9.8
	y = (population[:,1]+5)*9.8
#        print x
#        print y
#	print "\n"
        line.set_xdata(x)
        line.set_ydata(y)
        fig.canvas.draw()
	save()
        
def plot_function(minimum, maximum, dif):
    def fitness_two(x,y):
	sol = np.array([x,y])
	return function_fitness(sol)

    dx = dy = dif
    x = np.arange(minimum, maximum, dx)
    y = np.arange(minimum, maximum, dy)
    X,Y = meshgrid(x, y)
    Z = fitness_two(X, Y)
    global fig
    fig = plt.figure()
    ax = subplot(111)
    x, y = (np.random.rand(2, 50))*100
    ea.initPopulation(50)
    global eval
    eval=0
    population = ea.population()
    x = (population[:,0]+5)*9.8
    y = (population[:,1]+5)*9.8
#    print x
#    print y
#    print "\n"
    global line
    line, = ax.plot(x, y, 'wo')
    im = imshow(Z, cmap=cm.jet)
    im.set_interpolation('bilinear')
    save()
    aspects.with_wrap(measureFitness, SSGA.updateWorst)
    ea.run(numberOfTimeSteps)
    aspects.without_wrap(measureFitness, SSGA.updateWorst)
    # Clear the figure to make way for the next image.
    plt.clf()

plot_function(-5, 5, 0.1)
# Now that we have graphed images of the dataset, we will stitch them
# together using Mencoder to create a movie.  Each image will become
# a single frame in the movie.
#
# We want to use Python to make what would normally be a command line
# call to Mencoder.  Specifically, the command line call we want to
# emulate is (without the initial '#'):
# mencoder mf://*.png -mf type=png:w=800:h=600:fps=25 -ovc lavc -lavcopts vcodec=mpeg4 -oac copy -o output.avi
# See the MPlayer and Mencoder documentation for details.

command = ('mencoder',
           'mf://*.png',
           '-mf',
           'type=png:w=800:h=600:fps=25',
           '-ovc',
           'lavc',
           '-lavcopts',
           'vcodec=mpeg4',
           '-oac',
           'copy',
           '-o',
           'output.avi')

#os.spawnvp(os.P_WAIT, 'mencoder', command)

print "\n\nabout to execute:\n%s\n\n" % ' '.join(command)
subprocess.check_call(command)

print "\n\n The movie was written to 'output.avi'"

print "\n\n You may want to delete *.png now.\n\n"

