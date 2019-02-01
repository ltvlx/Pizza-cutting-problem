# Pizza cutting problem
The solution would be to optimize the layout of slices using genetic algorithm.


### Algorithm description:
0. Pre-calculate the available slices based on L and H.
1. Generate the initial population by going through the pizza cells and trying to put each slice in a random order.  
   The direction of walking is left-to-right, up-to-down.
2. Calculate the scores of each individual as the number of used cells
3. Select x% best and create a new generation via crossovers and mutations
4. Repeat operations 2-3 until the exit criterion is not satisfied.


### Progress of development:
* ~~Layout generator~~
* ~~Field drawer~~
* ~~Layout drawer~~
* ~~Generalized layout generator that can start from an incomplete layout~~
* Crossover procedure
* ~~Mutation procedure~~  
* ~~Put everything inside a Class environment to avoid passing problem parameters within procedures~~


### Open questions:
How to crossover two individuals?
How to mutate an individual?  
Why would the ideas below lead to the convergence?  
Why wouldn't it force to converge to a local maximum?  
How to formulate the idea of keeping the densely-filled areas of a layout when performing a crossover?  

Idea of mutations:  
Go through some of unused cells and remove adjacent slices. Then, try to fill them again.
This would help to reconfigure slices near the area, where cells became unreachable.

Idea of crossovers 1:  
Encode layout (genotype) as a dictionary {position: 'k-th slice'}. From the best x%, select two random individuals A and B. Calculate all their common genes (pos, k) pairs and remove y% of them + z% of other genes.

Idea of crossovers 2:  
Adaptation of one-point crossover procedure from [1] (see p. 53).  
Select a horizontal or a vertical line such that it splits pizza in two non-empty pieces.
For each of two individuals A and B, select sub-layouts for which slices lie strictly within the left or right piece.
Those slices intersecting the line are dropped.  
Combine left_A with right_B and left_B with right_A, fill the gaps between lefts and rights.


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


[1] A. E. Eiben and J. E. Smith, __Introduction to Evolutionary Computing__, 2nd ed. Springer, 2015
