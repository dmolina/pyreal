Feature: SSGA Crossover

    Scenario: Crossover with itself
	Given I have a SSGA algorithm
	When I init the population with 50
	When I set the same parent as mother
	When I cross with alpha 0
	Then the children is the same

   Scenario: NAM Select Parents
	Given I have a SSGA algorithm
	When I init the population with 50
	When I set randomly two parents
	When I use in crossover pseudorandoms=0
	Then the children is between them

    Scenario: Crossing with alpha=0.5 
	Given I have a SSGA algorithm
	When I init the population with 50
	When I set randomly two parents
	When I cross with alpha 0
	Then the children is between them
