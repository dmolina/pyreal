Feature: SSGA Crossover
    Check for BLX-0 than a crossover of a individual with itself is the same
    parent, and that offspring of a crossover are always between their
    parents

    Scenario: Crossover with itself
	Given I have a SSGA algorithm
	When I init the population with 50 individuals
	When I set the same parent as mother
	When I cross with alpha 0
	Then the children is the same

    Scenario: Crossing with alpha=0 is between them
	Given I have a SSGA algorithm
	When I init the population with 50 individuals
	When I set randomly two parents
	When I cross with alpha 0
	Then the children is between them

   Scenario: Checking crossover with seudorandoms and alpha=0
	Given I have a SSGA algorithm
	When I init the population with 50 individuals
	When I set randomly two parents
	When I use pseudorandoms=<seudo_random>
	When I cross with alpha 0
	Then the children is equals to the <criterion> of its parents

    Examples:
	| seudo_random | criterion |
	|   0          |  minimum  | 
	|   1          |  maximum  |
	|   0.5        |  mean     |
    
   Scenario: Checking crossover with alpha=0
	Given I have a SSGA algorithm
	When I init the population with 50 individuals
	When I set randomly two parents
	When I cross with alpha 0
	Then the children is equals to the mean of its parents
