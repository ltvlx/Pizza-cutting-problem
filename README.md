# Pizza cutting problem
The solution would be to optimize the layout of slices using genetic algorithm.


### Algorithm description:
0. Pre-calculate the available slices based on L and H.
1. Generate the initial population by going through the pizza cells and trying to put each slice in a random order.
   The direction of walking is left-to-right, up-to-down.
2. Calculate the scores of each individual as the number of used cells
3. Select x% best and create a new generation via crossover with mutations
(take an individual, remove y% of the slices, fill the rest with random procedure)
4. Repeat operations 2-3 until the exit criterion is not satisfied.


### Progress of development:
* ~~Layout generator~~
* ~~Field drawer~~
* Layout drawer
* Generalized layout generator that can start from an incomplete layout
* Crossover procedure
* Mutation procedure


### Open questions:
How to crossover two individuals?
How to mutate an individual?


### Additional thoughts:
* Some cells might be unreachable. Write an algorithm that calculates them and then just ignore them?
* Create the initial population with filling everything with maximum (or minimum) possible slices size?
* Insert a probability of randomly skipping a cell without any ingridients?
* Create the layout in random direction? (As opposed to left-to-right up-to-down)


### Helpful links:
Read about the contest:
https://codingcompetitions.withgoogle.com/hashcode

Join the team:
https://hashcodejudge.withgoogle.com/#join-team/5244709622513664/sX-bzEaQ6Ceq1q03UxMN0mTCv51kh9ue0SPu44dAEY4

Cutting stock problem solved via genetic algorithm:
https://github.com/fabiofdsantos/2d-cutting-stock-problem

Knapsack problem solved via genetic algorithm:
http://www.nils-haldenwang.de/computer-science/computational-intelligence/genetic-algorithm-vs-0-1-knapsack
