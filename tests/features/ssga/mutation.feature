Feature: SSGA Mutation

    Scenario: Mutation 
	Given I have a SSGA algorithm
	When I set the mutation rate to <mutation_rate>
	When I apply the mutation to <num_select> individuals
	Then about <num_expected> individuals have been modified with range error <diff>

    Examples:
	| mutation_rate | num_select | num_expected | diff | 
	|       0       |      100   |    0          |  0  |
	|       1       |       10   |   10          |  0  |
	|       0.5     |       20   |   10          |  3  | 
	|       0.5     |      100   |   50          | 20  | 
	|       0.1     |      100   |   10          | 20  | 

    Scenario: Mutation of one gene
	Given I have a SSGA algorithm
	When I set the mutation rate to 1
	When I apply the mutation to 10 individuals
	Then the mutated individuals differ only in 1 gen

