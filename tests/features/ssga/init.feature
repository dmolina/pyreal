Feature: SSGA Init
    In order to test SSGA we test the 

    Scenario: Init Population
	Given I have a SSGA algorithm
	When I init the population with 50
	Then popsize is right
	and dimension for each individual is right
	and fitness is initialized
	and all fitness values are different
