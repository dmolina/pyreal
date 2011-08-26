from numpy import random

randreal=random.uniform
rand=randreal
randint=random.randint

#def randreal(min, max, size):
#    """
#    Return a random vector of dim values, with a uniform value between [min,max] 
#
#    min -- minimum value
#    max -- maximum value
#    size -- length of the resulting vector
#    """
#    return random.uniform(min, max, size)
#
#def rand(min, max, size):
#    return random.randreal(min, max, size)
#
#def randint(min, max, size):
#    """
#    Return a integer random vector of dim values, with a uniform value between [min,max] 
#
#    min -- minimum value
#    max -- maximum value
#    size -- length of the resulting vector
#    """
#    return random.randint(min, max, size)

#def randint(max, size):
#    return random.randint(max, size)
#
#def uniform(low,high,total):
#    return random.uniform(low,high,total)
#
#def rand():
#    return random.rand()
#
def randbool(size):
    """
    Return a boolean random of size values
    
    size -- length of the resulting vector
    """
    return random.rand(size)<=0.5
    

