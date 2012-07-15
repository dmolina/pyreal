Feature: SSGA Init
    In order to test SSGA we test that the init population has
    the right popsize, dimension, and that initial fitness 
    between the individuals are different. 

    Scenario: Init Population
	Given I have a SSGA algorithm for dimension <dimension>
	When I init the population with <popsize> individuals 
	Then the population size is <popsize>
	Then dimension for each individual is <dimension>
	Then fitness is initialized
	Then all fitness values are different

    Examples:
	|  popsize | dimension |
	|    10    |    10     |
	|    50    |    10     |
	|   100    |    10     |
	|    10    |    30     |
	|    50    |    30     |
	|   100    |    30     |

