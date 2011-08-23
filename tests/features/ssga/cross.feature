Feature: SSGA Crossover

    Scenario: Crossover with itself
	Given I have a SSGA algorithm
	When I init the population with 50
	When I set the same parent as mother
	When I cross with alpha 0
	Then the children is the same

   Scenario: Checking crossover with seudorandoms and alpha=0
	Given I have a SSGA algorithm
	When I init the population with 50
	When I set randomly two parents
	When I use pseudorandoms=<seudo_random>
	When I cross with alpha 0
	Then the children is equals to the <criterion> of its parents

    Examples:
	| seudo_random | criterion |
	|   0          |  minimum  | 
	|   1          |  maximum  |
	|   0.5        |  mean     |
    
    Scenario: Crossing with alpha=0 is between them
	Given I have a SSGA algorithm
	When I init the population with 50
	When I set randomly two parents
	When I cross with alpha 0
	Then the children is between them
