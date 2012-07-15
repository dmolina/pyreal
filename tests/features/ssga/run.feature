Feature: SSGA run
    Check two fundamental features of the algorithm. First, 
    than the evaluations number is the right, and that
    it its elitism. 

    Scenario: SSGA runs implies a good 
	Given I have a SSGA algorithm
	When I init the population with <population_size>
	When I run the algorithm during <num_itera> iterations
	Then they were evaluated <num_eval> solutions

    Examples:
	| population_size | num_itera | num_eval |
	|    50           |   1000    |   1000   |
	|    20           |   1000    |   1000   |
	|    50           |   2500    |   2500   |
	|    50           |    100    |    100   |

    Scenario: Run of a SSGA the population evolutes well
	Given I have a SSGA algorithm
	When I init the population with 50
	When I study the evolution of the <individual> individual
	When I run the algorithm during <num_itera> iterations
	Then its fitness is always better

    Examples:
	| individual | num_itera |
	|    best    |  1000     |
	|    worst   |  1000     |
	|    mean    |  1000     |
