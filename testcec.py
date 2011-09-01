#import libhello
#print libhello.greet()
#planet = libhello.World()
#planet.set('howdy')
#print planet.greet()
import libpycec2005 as cec2005
import numpy as np

for f in range(1,26):
    cec2005.config(f, 30)
    print cec2005.isBound()
    x = np.random.uniform(-5.0, 5.0, 30)
    x = np.zeros(30)
    print cec2005.evaluate(x)
