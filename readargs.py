from optparse import OptionParser

class ArgsCEC05:

    """
    This class allow us to get the fitness and dimension parameter
    """
    def __init__(self):
	self.parser = OptionParser()
    	self.parser.add_option("-f", "--function", action="store", type="int", dest="function", help="set the function to optimise", metavar="FUNCTION")
    	self.parser.add_option("-d", "--dimension", action="store", type="int", dest="dimension", help="set the dimensionality (2|10|30|50)", metavar="FUNCTION")
    	self.parser.add_option("-t", "--times", action="store", type="int", dest="time", help="set the run number", metavar="FUNCTION")

	(options,args)=self.parser.parse_args()

	self.options = options
        self.error = False
    
        if options.function is None or options.dimension is None:
	   self.error = True
        else:
	    fun = options.function
	    dim = options.dimension
        
            if not self.isFunctionValide(fun):
                print "option function: invalid value: '%d'" %fun
		self.error = True

            if not self.isDimensionValide(dim):
                print "option dimension: invalid value: '%d'" %dim
                self.error = True

	    if options.time is None:
		self.time = 25
	    else:
		self.time = options.time

            if not self.isTimeValide(self.time):
                print "option run: invalid value: '%d'" %run
                self.error = True


    def isFunctionValide(self, fun):
        return (fun >= 0 and fun <= 25)

    def isTimeValide(self, times):
        return (times > 0 and times <= 25)
    
    def isDimensionValide(self,dim):
        return dim in [2, 10, 30, 50]

    def help(self):	
	self.parser.print_help()

    def print_help_exit(self):
	self.parser.print_help()
	self.parser.exit()

    @property
    def hasError(self):
	return self.error

    @property
    def function(self):
	return self.options.function

    @property
    def dimension(self):
	return self.options.dimension

    @property
    def times(self):
	return self.time
