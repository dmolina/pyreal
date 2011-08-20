Feature: SSGA NNAM

    Scenario: NAM Select the far away parent
	Given I have a SSGA algorithm
	When I init the population with 50
	When I select parents with tournament size 49
	Then the parent or the mother is the furthest

    Scenario: NAM selects different parents 
	Given I have a SSGA algorithm
	When I init the population with <popsize>
	When I select parents with tournament size <tournament_size>
	Then the parents are different after <numruns> tests

    Examples:
	| popsize | tournament_size | numruns |
	|     50  |  3              | 300     |
	|      3  |  2              | 300     |
	|      2  |  1              |   2     |
