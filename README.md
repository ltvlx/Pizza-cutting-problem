# Pizza cutting problem
A solution to the practice round problem of Google HashCode 2019.


### Algorithm description:
0. Pre-calculate the available slices based on L and H.
1. Generate the initial population by going through the pizza cells and trying to put each slice in a random order.  
   The direction of walking is left-to-right, up-to-down.
2. Calculate the scores of each individual as the number of used cells
3. Select x% best and create a new generation via recombinations and mutations
4. Repeat operations 2-3 until the exit criterion is not satisfied.


### Progress of development:
* ~~Layout generator~~
* ~~Field drawer~~
* ~~Layout drawer~~
* ~~Generalized layout generator that can start from an incomplete layout~~
* ~~Mutation procedure~~
* ~~Put everything inside a Class environment to avoid passing problem parameters within procedures~~
* ~~Recombination procedure~~
* ~~Selection procedure~~
* ~~Procedure to create generations~~


### Open questions:
How to improve the recombination to avoid inefficient combination in the area of cuts?

Idea of mutations (implemented):
Go through some of unused cells and remove adjacent slices. Then, try to fill them again.
This would help to reconfigure slices near the area, where cells became unreachable.

Idea of recombination 1 (implemented):
Adaptation of one-point crossover procedure from [1] (see p. 53).  
* Select a horizontal and a vertical line that split the pizza in 4 non-empty pieces.
* Select a pattern of picking 2 zones out of that 4 pieces. There are 7 unique ways of picking those zones. 
* For each of two individuals A and B, put all slices that lie strictly within zone 1 and zone 2 into separate sub-layouts A_1, A_2, B_1, and B_2. Slices that intersect the lines are dropped.  
* Create new layouts by combining A_1 with B_2 and B_1 with A_2. Fill the gaps created by dropped slices.

The recombination prduces individuals that are not exceeding the efficiency of their parents.  
__How to improve the procedure of combining sub-layouts A_1 and B_2?__

Idea of recombination 2:  
Select a square block from indiviudal A's layout and swap it with the same block from individual B.  

Idea of recombination 3:  
Encode layout (genotype) as a dictionary {position: 'k-th slice'}. From the best x%, select two random individuals A and B. Calculate all their common genes (pos, k) pairs and remove y% of them + z% of other genes.


### Links to the tests of methods:
[See link](tests/README.md)

### Additional thoughts:
* ~~Some cells might be unreachable. Write an algorithm that calculates them and then just ignore them?~~  
Too much work for a questionable profit.
* Create the initial population with filling everything with maximum (or minimum) possible slices size?
* Insert a probability of randomly skipping a cell without any ingridients?
* ~~Create the layout in random direction? (As opposed to left-to-right up-to-down)~~  
A test has shown that it reduces efficiency a lot.  
Instead, filling the layout in spiral order might be helpful.


### Helpful links:
Read about the contest:  
https://codingcompetitions.withgoogle.com/hashcode

Join the team:  
https://hashcodejudge.withgoogle.com/#join-team/5244709622513664/sX-bzEaQ6Ceq1q03UxMN0mTCv51kh9ue0SPu44dAEY4

Cutting stock problem solved via genetic algorithm:  
https://github.com/fabiofdsantos/2d-cutting-stock-problem

Knapsack problem solved via genetic algorithm:  
http://www.nils-haldenwang.de/computer-science/computational-intelligence/genetic-algorithm-vs-0-1-knapsack

Cython documentation  
https://cython.org/#documentation


[1] A. E. Eiben and J. E. Smith, __Introduction to Evolutionary Computing__, 2nd ed. Springer, 2015
