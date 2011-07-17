Feature: SSGA
    In order to test SSGA
    and 
    in order to test NAM crossover operator

    Scenario: Init Population
	Given I have a SSGA algorithm
	When I init the population with 50
	Then popsize is right
	and dimension for each individual is right
	and fitness is initialized
	and all fitness values are different

    Scenario: NAM Select Parents 
	Given I have a SSGA algorithm
	When I init the population with 50
	When I select parents with tournament size 49
	Then the parent or the mother is the furthest

    Scenario: NAM Select Parents
	Given I have a SSGA algorithm
	When I init the population with 3
	Then the parents are different after 300 tests

    Scenario: NAM Select Parents
	Given I have a SSGA algorithm
	When I init the population with 2
	Then the parents are different after 2 tests

    Scenario: Crossover with itself
	Given I have a SSGA algorithm
	When I init the population with 50
	When I set the same parent as mother
	When I cross with alpha 0
	Then the children is the same

    Scenario: Crossover with mean 
	Given I have a SSGA algorithm
	When I init the population with 50
	When I set randomly two parents
	When I cross with alpha 0
	Then the children is between them
